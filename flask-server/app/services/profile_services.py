from flask import jsonify

from ..data_mappers.profile_mapper import ProfileMapper


class ProfileService:
    @staticmethod
    def get_all_profiles(db_session=None):
        """
        Retrieves a list of all profiles, with optional filtering and sorting based on query parameters.

        Args:
            db_session: Optional database session to be used in tests.

        Returns:
            A JSON response containing the list of profiles with a 200 status code.
        """
        profiles = ProfileMapper.get_all_profiles(db_session=db_session)
        return jsonify(profiles), 200

    @staticmethod
    def get_profile(user_id, db_session=None):
        """
        Retrieves a specific profile by its associate user ID.

        Args:
            user_id: The ID of the user to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            A JSON response with the profile data if found, otherwise a 404 error with a message.
        """
        profile = ProfileMapper.get_profile(user_id, db_session=db_session)
        if profile:
            return jsonify(profile), 200
        return jsonify({"error": "profile not found"}), 404

    @staticmethod
    def create_profile(data, db_session=None):
        """
        Creates a new profile with the provided data.

        Args:
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A JSON response with the success message and newly created listing ID, or a 400 error if the title is missing.
        """
        if not data.get("user_id") or not data.get("first_name") or not data.get("last_name"):
            return jsonify({"error": "Required fields are missing"}), 400
        profile_id = ProfileMapper.create_profile(data, db_session=db_session)
        return jsonify({"message": "profile created", "profile_id": profile_id}), 201

    @staticmethod
    def update_profile(profile_id, data, db_session=None):
        """
        Updates an existing profile by its ID with the provided data.

        Args:
            profile_id: The ID of the profile to update.
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A JSON response with a success message if the profile was updated, or a 404 error if the profile was not found.
        """
        updated_rows = ProfileMapper.update_profile(profile_id, data, db_session=db_session)
        if updated_rows:
            return jsonify({"message": "profile updated"}), 200
        return jsonify({"error": "profile not found"}), 404

    @staticmethod
    def delete_profile(user_id, db_session=None):
        """
        Deletes a profile by its ID.

        Args:
            user_id: The ID of the user associated with the profile to delete.
            db_session: Optional database session to be used in tests.

        Returns:
            A JSON response with a success message if the profile was deleted, or a 404 error if the profile was not found.
        """
        deleted_rows = ProfileMapper.delete_profile(user_id, db_session=db_session)
        if deleted_rows:
            return jsonify({"message": "profile deleted"}), 200
        return jsonify({"error": "profile not found"}), 404
