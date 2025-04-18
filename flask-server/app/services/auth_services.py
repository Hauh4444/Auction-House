from flask import jsonify, session, Response
from flask_login import login_user, logout_user, current_user

from datetime import datetime, timedelta
import os, jwt

from .session_services import SessionService
from .email_services import EmailService
from ..data_mappers import AuthMapper, ProfileMapper, UserMapper
from ..utils.password import hash_password
from ..utils.logger import setup_logger

logger = setup_logger(name="auth_logger", log_file="logs/auth.log")


class AuthService:
    @staticmethod
    def check_auth_status():
        """
        Checks the authentication status of the current session.

        Returns:
            Response: A JSON response containing the authentication status and user details.
                Status code 200 if authenticated, 401 if not.
        """
        if not current_user.is_authenticated:
            response_data = {"error": "Error user is not authenticated", "authenticated": False}
            logger.error(msg=f"User is not authenticated")
            return Response(response=jsonify(response_data).get_data(), status=401, mimetype="application/json")

        response_data = {"message": "User is authenticated", "authenticated": True, "id": current_user.id, "role": current_user.role}
        logger.info(msg=f"User: {current_user.id} is authenticated as: {current_user.role}")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def create_user(data, db_session=None):
        """
        Creates a new user account.

        Args:
            data (dict): A dictionary containing the user's information (username, password, email, etc.).
            db_session (Optional[Session]): A database session used for testing.

        Returns:
            Response: A JSON response indicating success or failure.
                Returns 201 status if user created successfully or 409 for conflicts.
        """
        user_data = {"username": data.get("username"), "password_hash": hash_password(password=data.get("password")), "email": data.get("email")}
        user_id = AuthMapper.create_user(data=user_data, db_session=db_session)
        if not user_id:
            response_data = {"error": "Error creating user"}
            logger.error(msg=f"Failed creating user with data: {', '.join(f'{k}={v!r}' for k, v in user_data.items())}")
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

        profile_data = {"user_id": user_id, "first_name": data.get("first_name"), "last_name": data.get("last_name")}
        profile_id = ProfileMapper.create_profile(data=profile_data, db_session=db_session).get_json().get("profile_id")
        if not profile_id:
            response_data = {"error": "Error creating profile"}
            logger.error(msg=f"Failed creating profile with data: {', '.join(f'{k}={v!r}' for k, v in profile_data.items())}")
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

        response_data = {"message": "User registered successfully", "user_id": user_id, "profile_id": profile_id}
        logger.info(msg=f"User: {user_id} and profile: {profile_id} registered successfully with data: {data}")
        return Response(response=jsonify(response_data).get_data(), status=201, mimetype="application/json")


    @staticmethod
    def login(data, db_session=None):
        """
        Authenticates and logs in a user based on the provided username and password.

        Args:
            data (dict): A dictionary containing 'username' and 'password' keys.
            db_session (Optional[Session]): A database session used for testing.

        Returns:
            Response: A JSON response with a success message and user data if login is successful.
                Returns 400 if username or password is missing, 422 if credentials are invalid.
        """
        user = AuthMapper.get_user_by_username(username=data.get("username"), db_session=db_session)
        if not user or not user.password_hash == hash_password(data.get("password")):
            response_data = {"error": "Invalid username or password"}
            logger.error(msg=f"Invalid username: {data.get('username')} or password: {data.get('password')}")
            return Response(response=jsonify(response_data).get_data(), status=422, mimetype="application/json")

        session.update(user_id=user.id, role=user.role)
        login_user(user=user, remember=True)
        current_user.is_active = True
        AuthMapper.update_last_login(user_id=current_user.id, db_session=db_session)
        SessionService.create_session(db_session=db_session)

        response_data = {"message": "Login successful", "user": user}
        logger.info(msg=f"Login successful for user: {user.id}")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def logout():
        """
        Logs out the currently authenticated user.

        Returns:
            Response: A JSON response indicating the result of the logout operation.
                Status 200 if logout was successful.
        """
        logger.info(msg=f"Logout for user: {current_user}")

        logout_user()
        session.clear()
        current_user.is_active = False

        response_data = {"message": "Logout successful"}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def password_reset_request(db_session=None):
        """
        Handles a password reset request by generating and sending a reset email.

        Returns:
            Response: A JSON response indicating success or failure in sending the password reset email.
                Returns 202 if email was successfully sent, 404 if profile or user not found.
        """
        reset_token = jwt.encode({
            'user_id': current_user.id,
            'exp': datetime.now() + timedelta(hours=1)
        }, os.getenv('SECRET_KEY'), algorithm='HS256')
        reset_link = f"{os.getenv('FRONTEND_URL')}/reset_password?token={reset_token}"
        subject = "Password Reset Request"
        body = f"Your password reset link is: {reset_link}"

        profile = ProfileMapper.get_profile(user_id=current_user.id, db_session=db_session)
        if not profile:
            response_data = {"error": "Profile not found"}
            logger.error(msg=f"Profile not found for user: {current_user.id}")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        user = UserMapper.get_user(user_id=current_user.id, db_session=db_session)
        if not user:
            response_data = {"error": "User not found"}
            logger.error(msg=f"User not found with id: {current_user.id}")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        # Use EmailService to send the email
        mail_response = EmailService.send_email(subject, [user.get("email")], body)
        if not int(mail_response) == 202:
            response_data = {"error": "HTTP error sending email"}
            logger.error(msg=f"HTTP failure sending email to: {user.get('email')} body: {body}")
            return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")

        response_data = {"message": "Password reset email sent"}
        logger.info(msg=f"Password reset email sent to: {user.get('email')}")
        return Response(response=jsonify(response_data).get_data(), status=202, mimetype="application/json")


    @staticmethod
    def reset_user_password(reset_token, new_password, db_session=None):
        """
        Resets the user's password using a provided reset token.

        Args:
            reset_token (str): The token used to verify the password reset request.
            new_password (str): The new password to set for the user.
            db_session (Optional[Session]): A database session used for testing.

        Returns:
            Response: A JSON response indicating the result of the password reset operation.
                Returns 200 if password is successfully reset, 400 if the token is expired or invalid, 404 if user not found.
        """
        try:
            jwt.decode(reset_token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            response_data = {"error": "Reset token has expired"}
            logger.error(msg=f"Reset token: {reset_token} expired for user: {current_user.id}")
            return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")
        except jwt.InvalidTokenError:
            response_data = {"error": "Invalid reset token"}
            logger.error(msg=f"Invalid reset token: {reset_token} for user: {current_user.id}")
            return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")

        # Get the current user
        user = UserMapper.get_user(user_id=current_user.id, db_session=db_session)
        if not user:
            response_data = {"error": "User not found"}
            logger.error(msg=f"User not found with id: {current_user.id}")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        # Update the user's password
        updated_user_data = {"password_hash": hash_password(new_password)}
        updated_rows = UserMapper.update_user(user_id=current_user.id, data=updated_user_data, db_session=db_session)
        if not updated_rows:
            response_data = {"error": "Error updating user"}
            logger.error(msg=f"Error updating user: {current_user.id} with new password: {new_password}")
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

        response_data = {"message": "Password has been reset"}
        logger.info(msg=f"User: {current_user.id} successfully reset password to: {new_password}")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")
