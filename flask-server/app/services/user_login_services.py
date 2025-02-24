from flask import jsonify
from ..data_mappers.user_login_mapper import UserMapper
import hashlib


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
        if user and user["password_hash"] == UserLoginService.hash_password(password):
            # Update the last login timestamp
            UserMapper.update_last_login(user["user_id"])
            return jsonify({"message": "Login successful", "user": user}), 200
        return jsonify({"error": "Invalid username or password"}), 401

    @staticmethod
    def register_user(data):
        """
        Registers a new user by creating a new user record in the database.

        Args:
            data: A dictionary containing user details such as username, password_hash, email, etc.

        Returns:
            A JSON response with a success message and the newly created user ID, or a 400 error if registration fails.
        """
        if not data.get("username") or not data.get("password_hash") or not data.get("email"):
            return jsonify({"error": "Username, password, and email are required"}), 400
        
        # Create the new user in the database
        user_id = UserMapper.create_user(data)
        return jsonify({"message": "User registered successfully", "user_id": user_id}), 201

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
