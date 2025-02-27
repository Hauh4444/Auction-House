from flask import jsonify, session
from flask_login import login_user, logout_user, current_user

import hashlib

from .profile_services import ProfileService
from ..services.session_services import SessionService
from ..data_mappers.auth_mapper import AuthMapper


class AuthService:
    @staticmethod
    def check_auth_status():
        """
        Checks authentication status of the current session.

        Returns:
            A JSON response with the authentication status and user ID if authenticated, otherwise a 401 error.
        """
        if current_user.is_authenticated:
            return jsonify({"authenticated": True, "user": current_user.id}), 200
        return jsonify({"authenticated": False}), 401

    @staticmethod
    def create_user(data, db_session=None):
        """
        Creates a new user account.

        Args:
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A JSON response indicating success with the user ID or an error message.
        """
        data["password_hash"] = AuthService.hash_password(password=data["password"])
        if not data.get("username") or not data.get("password_hash") or not data.get("email"):
            return jsonify({"error": "Username, password, and email are required"}), 400

        ProfileService.create_profile(data=data, db_session=db_session)
        user_id = AuthMapper.create_user(data=data, db_session=db_session)
        return jsonify({"message": "User registered successfully", "user_id": user_id}), 201

    @staticmethod
    def login_user(username, password, db_session=None):
        """
        Logs in a user by verifying their username and password.

        Args:
            username: The username of the user.
            password: The password provided by the user.
            db_session: Optional database session to be used in tests.

        Returns:
            A JSON response containing a success message and the user details if login is successful,
            or a 401 error if the username or password is incorrect.
        """
        user = AuthMapper.get_user_by_username(username=username, db_session=db_session)
        if user and user.password_hash == AuthService.hash_password(password=password):
            if user.__class__.__name__ == "User":
                AuthMapper.update_last_login(user_id=user.user_id, db_session=db_session)
                session["user_id"] = user.user_id
                session["role"] = "user"
            else:
                AuthMapper.update_last_login(user_id=user.staff_id, role=user.role, db_session=db_session)
                session["user_id"] = user.staff_id
                session["role"] = user.role
            user.is_active = True
            login_user(user=user, remember=True)
            SessionService.create_session(db_session=db_session)
            return jsonify({"message": "Login successful", "user": user}), 200
        return jsonify({"error": "Invalid username or password"}), 401

    @staticmethod
    def logout_user():
        """
        Logs out the currently logged-in user.

        Returns:
            A JSON response indicating the success of the logout operation.
        """
        current_user.is_active = False
        logout_user()
        session.clear()
        return jsonify({"message": "Logout successful"}), 200

    @staticmethod
    def hash_password(password):
        """
        Hashes the password using SHA256.

        Args:
            password: The password to hash.

        Returns:
            A hashed version of the password.
        """
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def password_reset_request(email):
        """
        Handles a password reset request.

        Args:
            email: The email of the user requesting a password reset.

        Returns:
            A JSON response indicating whether the request was successful.
        """
        return email

    @staticmethod
    def reset_user_password(reset_token, new_password):
        """
        Resets a user's password using a reset token.

        Args:
            reset_token: The token used to verify the password reset request.
            new_password: The new password to set for the user.

        Returns:
            A JSON response indicating whether the password reset was successful.
        """
        return reset_token, new_password
