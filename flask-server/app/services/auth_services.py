from flask import jsonify, session, Response
from flask_login import login_user, logout_user, current_user
import os
import jwt
import datetime

from .profile_services import ProfileService
from .session_services import SessionService
from ..data_mappers import AuthMapper
from ..utils import hash_password


class AuthService:
    @staticmethod
    def check_auth_status():
        """
        Checks authentication status of the current session.

        Returns:
            A Response object with the authentication status and user ID if authenticated, otherwise a 401 error.
        """

        if current_user.is_authenticated:
            data = {"authenticated": True, "user": current_user.id}
            response = Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')
            return response

        data = {"authenticated": False}
        response = Response(response=jsonify(data).get_data(), status=401, mimetype="application/json")
        return response


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
        data["password_hash"] = hash_password(password=data["password"])

        if not data.get("username") or not data.get("password_hash") or not data.get("email"):
            data = {"error": "Username, password, and email are required"}
            response = Response(response=jsonify(data).get_data(), status=400, mimetype='application/json')
            return response

        ProfileService.create_profile(data=data, db_session=db_session)
        user_id = AuthMapper.create_user(data=data, db_session=db_session)

        data = {"message": "User registered successfully", "user_id": user_id}
        response = Response(response=jsonify(data).get_data(), status=201, mimetype='application/json')
        return response


    @staticmethod
    def login_user(username, password, db_session=None):
        """
        Logs in a user by verifying their username and password.

        Args:
            username: The username of the user.
            password: The password provided by the user.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object containing a success message and the user details if login is successful,
            or a 401 error if the username or password is incorrect.
        """
        user = AuthMapper.get_user_by_username(username, db_session)
        if user and user.password_hash == hash_password(password):
            session["user_id"], session["role"] = (user.user_id, "user") if user.__class__.__name__ == "User" else (user.staff_id, user.role)
            AuthMapper.update_last_login(user_id=session["user_id"], role=session["role"] if "role" in session else "user", db_session=db_session)
            user.is_active = True
            login_user(user, remember=True)
            SessionService.create_session(db_session)

            data = {"message": "Login successful", "user": user}
            response = Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')
            return response

        data = {"error": "Invalid username or password"}
        response = Response(response=jsonify(data).get_data(), status=401, mimetype='application/json')
        return response


    @staticmethod
    def logout_user():
        """
        Logs out the currently logged-in user.

        Returns:
            A Response object indicating the success of the logout operation.
        """
        current_user.is_active = False
        logout_user()
        session.clear()

        data = {"message": "Logout successful"}
        response = Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')
        return response


    @staticmethod
    def password_reset_request(email):
        """
        Handles a password reset request.

        Args:
            email: The email of the user requesting a password reset.

        Returns:
            A Response object indicating whether the request was successful.
        """
        user = User.query.filter_by(email=email).first()
        if not user:
            return {"error": "User not found"}, 404

        reset_token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, os.getenv('SECRET_KEY'), algorithm='HS256')

        reset_link = f"{os.getenv('FRONTEND_URL')}/reset_password?token={reset_token}"
        subject = "Password Reset Request"
        body = f"Your password reset link is: {reset_link}"

        ###TODO: Implement email functionality
        send_email(email, subject, body)

        return {"message": "Password reset email sent"}, 200


    @staticmethod
    def reset_user_password(reset_token, new_password):
        """
        Resets a user's password using a reset token.

        Args:
            reset_token: The token used to verify the password reset request.
            new_password: The new password to set for the user.

        Returns:
            A Response object indicating whether the password reset was successful.
        """
        try:
            data = jwt.decode(reset_token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return {"error": "Reset token has expired"}, 400
        except jwt.InvalidTokenError:
            return {"error": "Invalid reset token"}, 400

        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        user.password = generate_password_hash(new_password)
        db.session.commit()

        return {"message": "Password has been reset"}, 200
