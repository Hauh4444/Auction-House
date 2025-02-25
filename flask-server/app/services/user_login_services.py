from flask import jsonify, session
from flask_login import login_user, logout_user, current_user

from ..data_mappers.user_login_mapper import UserMapper
from ..services.user_profile_services import UserProfileService
from datetime import datetime, date
import hashlib

class UserLoginService:
    @staticmethod
    def check_auth_status():
        """
        Checks authentication status of current session

        Returns:
            A JSON response with the authentication status and user id if authenticated, otherwise a 401 error
        """
        if current_user.is_authenticated:
            return jsonify({"authenticated": True, "user": current_user.id}), 200
        return jsonify({"authenticated": False}), 401

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
        if user and user.password_hash == UserLoginService.hash_password(password):
            UserMapper.update_last_login(user.user_id) # Update the last login timestamp
            login_user(user, remember=True) # Login User using flask login
            session["user_id"] = user.user_id  # Store user ID in session
            return jsonify({"message": "Login successful", "user": user}), 200
        return jsonify({"error": "Invalid username or password"}), 401

    @staticmethod
    def register_user(request):
        """
        Registers a new user by creating a new user record in the database.

        Args:
            request: A dictionary containing user details such as username, password_hash, email, etc.

        Returns:
            A JSON response with a success message and the newly created user ID, or a 400 error if registration fails.
        """
        data = request.json

        data["password_hash"] = UserLoginService.hash_password(data["password"])

        if not data.get("username") or not data.get("password_hash") or not data.get("email"):
            return jsonify({"error": "Username, password, and email are required"}), 400

        # Create the new user in the database
        user_id = UserMapper.create_user(data)
        return jsonify({"message": "User registered successfully", "user_id": user_id}), 201

    @staticmethod
    def logout_user():
        """
        Logs out the currently logged-in user.

        Returns:
            A JSON response indicating the success of the logout operation.
        """
        logout_user()  # Call Flask-Login's logout_user to clear the session
        session.clear()
        return jsonify({"message": "Logout successful"}), 200

    @staticmethod
    def hash_password(password):
        """
        Hash the password using SHA256.

        Args:
            password: The password to hash.

        Returns:
            A hashed version of the password.
        """
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def password_reset_request(email):
        return 404

    @staticmethod
    def reset_user_password(reset_token, new_password):
        return 404

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
    def update_user_details(user_id, data):
        """
        Updates the details of an existing user.

        Args:
            user_id: The ID of the user to update.
            data: A dictionary containing the fields to update.

        Returns:
            A JSON response with a success message if the user was updated, or a 404 error if the user was not found.
        """
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
        deleted_rows = UserMapper.delete_user(user_id)
        if deleted_rows:
            return jsonify({"message": "User deleted"}), 200
        return jsonify({"error": "User not found"}), 404
