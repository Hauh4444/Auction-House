from flask import jsonify
from ..data_mappers.user_profile_mapper import UserProfileMapper


class UserProfileService:
    @staticmethod
    def get_all_user_profiles(request):
        """
        Retrieves a list of all user profiles, with optional filtering and sorting based on query parameters.

        Args:
            request: The request object containing query parameters for filtering, sorting, and pagination.

        Returns:
            A JSON response containing the list of user profiles with a 200 status code.
        """
        user_profiles = UserProfileMapper.get_all_user_profiles(args=request.args)
        return jsonify(user_profiles), 200

    @staticmethod
    def get_user_profile_by_id(user_id):
        """
        Retrieves a specific user profile by its associate user ID.

        Args:
            user_id: The ID of the user to retrieve.

        Returns:
            A JSON response with the profile data if found, otherwise a 404 error with a message.
        """
        profile = UserProfileMapper.get_user_profile_by_id(user_id)
        if profile:
            return jsonify(profile), 200
        return jsonify({"error": "User profile not found"}), 404

    @staticmethod
    def create_user_profile(data):
        """
        Creates a new user profile with the provided data.

        Args:
            data: A dictionary containing the profile details such as user_id, first_name, last_name, etc.

        Returns:
            A JSON response with the success message and newly created profile ID, or a 400 error if the required fields are missing.
        """
        if not data.get("user_id") or not data.get("first_name") or not data.get("last_name"):
            return jsonify({"error": "Required fields are missing"}), 400
        profile_id = UserProfileMapper.create_user_profile(data)
        return jsonify({"message": "User profile created", "profile_id": profile_id}), 201

    @staticmethod
    def update_user_profile(profile_id, request):
        """
        Updates an existing user profile by its ID with the provided data.

        Args:
            profile_id: The ID of the profile to update.
            request: A dictionary containing the fields to update.

        Returns:
            A JSON response with a success message if the profile was updated, or a 404 error if the profile was not found.
        """
        data = request.json["data"]
        updated_rows = UserProfileMapper.update_user_profile(profile_id, data)
        if updated_rows:
            return jsonify({"message": "User profile updated"}), 200
        return jsonify({"error": "User profile not found"}), 404

    @staticmethod
    def delete_user_profile(profile_id):
        """
        Deletes a user profile by its ID.

        Args:
            profile_id: The ID of the profile to delete.

        Returns:
            A JSON response with a success message if the profile was deleted, or a 404 error if the profile was not found.
        """
        deleted_rows = UserProfileMapper.delete_user_profile(profile_id)
        if deleted_rows:
            return jsonify({"message": "User profile deleted"}), 200
        return jsonify({"error": "User profile not found"}), 404
