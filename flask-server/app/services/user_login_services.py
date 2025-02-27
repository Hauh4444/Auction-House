from flask import jsonify, session
from flask_login import login_user, logout_user, current_user

import hashlib

from ..data_mappers.user_login_mapper import UserMapper
from ..services.user_profile_services import UserProfileService
from ..services.session_services import SessionService


class UserLoginService:
    @staticmethod
    def get_user_by_id(user_id):
        """
        Retrieves a user by their ID.

        Args:
            user_id: The ID of the user to retrieve.

        Returns:
            A JSON response with the user details if found, otherwise a 404 error with a message.
        """
        user = UserMapper.get_user_by_id(user_id)
        if user:
            return jsonify(user), 200
        return jsonify({"error": "User not found"}), 404

    @staticmethod
    def get_user_by_username(username):
        """
        Retrieves a user by their username.

        Args:
            username: The username of the user to retrieve.

        Returns:
            A JSON response with the user details if found, otherwise a 404 error with a message.
        """
        user = UserMapper.get_user_by_username(username)
        if user:
            return jsonify(user), 200
        return jsonify({"error": "User not found"}), 404

    @staticmethod
    def create_user(request):
        """
        Creates a new user account.

        Args:
            request: The HTTP request containing the JSON payload with user details.

        Returns:
            A JSON response indicating success with the user ID or an error message.
        """
        data = request.json

        data["password_hash"] = UserLoginService.hash_password(data["password"])
        if not data.get("username") or not data.get("password_hash") or not data.get("email"):
            return jsonify({"error": "Username, password, and email are required"}), 400

        UserProfileService.create_user_profile(data)
        user_id = UserMapper.create_user(data)
        return jsonify({"message": "User registered successfully", "user_id": user_id}), 201

    @staticmethod
    def update_user(user_id, request):
        """
        Updates user information.

        Args:
            user_id: The ID of the user to update.
            request: The HTTP request containing the JSON payload with updated details.

        Returns:
            A JSON response indicating success or an error message if the user is not found.
        """
        data = request.json

        updated_rows = UserMapper.update_user(user_id, data)
        if updated_rows:
            return jsonify({"message": "User updated successfully"}), 200
        return jsonify({"error": "User not found"}), 404

    @staticmethod
    def delete_user(user_id):
        """
        Deletes a user by their ID.

        Args:
            user_id: The ID of the user to delete.

        Returns:
            A JSON response with a success message if the user was deleted, or a 404 error if the user was not found.
        """
        UserProfileService.delete_user_profile(user_id)
        deleted_user_rows = UserMapper.delete_user(user_id)
        if deleted_user_rows:
            return jsonify({"message": "User deleted"}), 200
        return jsonify({"error": "User not found"}), 404

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
    def login_user(username, password):
        """
        Logs in a user by verifying their username and password.

        Args:
            username: The username of the user.
            password: The password provided by the user.

        Returns:
            A JSON response containing a success message and the user details if login is successful,
            or a 401 error if the username or password is incorrect.
        """
        user = UserMapper.get_user_by_username(username)
        print(user)
        if user and user.password_hash == UserLoginService.hash_password(password):
            # Update the last login timestamp
            UserMapper.update_last_login(user.user_id)
            # Login User using Flask-Login
            login_user(user, remember=True)
            # Store user ID in Flask-Session
            session["user_id"] = user.user_id
            # Call create session service to store session
            SessionService.create_session()
            return jsonify({"message": "Login successful", "user": user}), 200
        return jsonify({"error": "Invalid username or password"}), 401

    @staticmethod
    def logout_user():
        """
        Logs out the currently logged-in user.

        Returns:
            A JSON response indicating the success of the logout operation.
        """
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
