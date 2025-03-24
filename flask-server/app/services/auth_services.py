from flask import jsonify, session, Response
from flask_login import login_user, logout_user, current_user

from datetime import datetime, timedelta
import os, jwt

from pygments.lexers.jsonnet import jsonnet_function_token

from .profile_services import ProfileService
from .session_services import SessionService
from .email_services import EmailService
from ..data_mappers import AuthMapper, ProfileMapper, UserMapper
from ..utils.password import hash_password


class AuthService:
    @staticmethod
    def check_auth_status():
        """
        Checks authentication status of the current session.

        Returns:
            A Response object with the authentication status and user ID if authenticated, otherwise a 401 error.
        """

        if not current_user.is_authenticated:
            response_data = {"error": "Error user is not authenticated", "authenticated": False}
            return Response(response=jsonify(response_data).get_data(), status=401, mimetype="application/json")

        response_data = {"message": "User is authenticated", "authenticated": True, "user": current_user.id}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def create_user(data, db_session=None):
        """
        Creates a new user account.

        Args:
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object indicating success with the user ID or an error message.
        """
        if not data.get("username") or not data.get("password") or not data.get("email"):
            response_data = {"error": "Username, password, and email are required"}
            return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")

        user_data = {"username": data.get("username"), "password_hash": hash_password(password=data.get("password")), "email": data.get("email")}
        user_id = AuthMapper.create_user(data=user_data, db_session=db_session)

        if not user_id:
            response_data = {"error": "Error creating user"}
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

        profile_data = {"user_id": user_id, "first_name": data.get("first_name"), "last_name": data.get("last_name")}
        profile_id = ProfileService.create_profile(data=profile_data, db_session=db_session).get_json().get("profile_id")

        if not profile_id:
            response_data = {"error": "Error creating profile"}
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

        response_data = {"message": "User registered successfully", "user_id": user_id, "profile_id": profile_id}
        return Response(response=jsonify(response_data).get_data(), status=201, mimetype="application/json")


    @staticmethod
    def login_user(data, db_session=None):
        """
        Logs in a user by verifying their username and password.

        Args:
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object containing a success message and the user details if login is successful,
            or a 401 error if the username or password is incorrect.
        """
        if not data.get("username") or not data.get("password"):
            return jsonify({"error": "Username and password are required"}), 400

        user = AuthMapper.get_user_by_username(data.get("username"), db_session)

        if not user or not user.password_hash == hash_password(data.get("password")):
            response_data = {"error": "Invalid username or password"}
            return Response(response=jsonify(response_data).get_data(), status=422, mimetype="application/json")

        if user.__class__.__name__ == "User":
            session.update(user_id=user.user_id, role="user")
        else:
            session.update(user_id=user.staff_id, role=user.role)

        login_user(user, remember=True)
        user.is_active = True

        AuthMapper.update_last_login(user_id=session.get("user_id"), role=session.get("role"), db_session=db_session)
        SessionService.create_session(db_session)

        response_data = {"message": "Login successful", "user": user}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def logout_user():
        """
        Logs out the currently logged-in user.

        Returns:
            A Response object indicating the success of the logout operation.
        """
        logout_user()
        session.clear()
        current_user.is_active = False

        response_data = {"message": "Logout successful"}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def password_reset_request(db_session=None):
        """
        Handles a password reset request.

        Returns:
            A Response object indicating whether the request was successful.
        """
        reset_token = jwt.encode({
            'user_id': session.get("user_id"),
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, os.getenv('SECRET_KEY'), algorithm='HS256')

        reset_link = f"{os.getenv('FRONTEND_URL')}/reset_password?token={reset_token}"
        subject = "Password Reset Request"
        body = f"Your password reset link is: {reset_link}"

        profile = ProfileMapper.get_profile(user_id=session.get("user_id"), db_session=db_session)
        if not profile:
            response_data = {"error": "Profile not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        # Use EmailService to send the email
        EmailService.send_email(subject, [profile.get("email")], body)

        response_data = {"message": "Password reset email sent"}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def reset_user_password(reset_token, new_password, db_session=None):
        """
        Resets a user's password using a reset token.

        Args:
            reset_token: The token used to verify the password reset request.
            new_password: The new password to be set for the user.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object indicating whether the password reset was successful.
        """
        try:
            jwt.decode(reset_token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            response_data = {"error": "Reset token has expired"}
            return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")
        except jwt.InvalidTokenError:
            response_data = {"error": "Invalid reset token"}
            return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")

        # Get the current user
        user = UserMapper.get_user(user_id=session.get("user_id"), db_session=db_session)

        if not user:
            response_data = {"error": "User not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        # Update the user's password
        updated_user_data = {
            "password_hash": hash_password(new_password)
        }
        updated_rows = UserMapper.update_user(user_id=session.get("user_id"), data=updated_user_data, db_session=db_session)

        if not updated_rows:
            response_data = {"error": "User not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Password has been reset"}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")
