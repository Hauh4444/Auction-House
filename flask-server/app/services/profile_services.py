from flask import jsonify, Response, session

from ..data_mappers import ProfileMapper


class ProfileService:
    @staticmethod
    def get_profile(db_session=None):
        """
        Retrieves a specific profile by its associate user ID.

        Args:
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object with the profile data if found, otherwise a 404 error with a message.
        """
        profile = ProfileMapper.get_profile(user_id=session.get("user_id"), db_session=db_session)

        if not profile:
            response_data = {"error": "Profile not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Profile found", "profile": profile}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def create_profile(data, db_session=None):
        """
        Creates a new profile with the provided data.

        Args:
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object with the success message and newly created listing ID, or a 400 error if the title is missing.
        """
        profile_id = ProfileMapper.create_profile(data=data, db_session=db_session)

        if not profile_id:
            response_data = {"error": "Error creating profile"}
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

        response_data = {"message": "Profile created", "profile_id": profile_id}
        return Response(response=jsonify(response_data).get_data(), status=201, mimetype="application/json")
        

    @staticmethod
    def update_profile(data, db_session=None):
        """
        Updates an existing profile by its ID with the provided data.

        Args:
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object with a success message if the profile was updated, or a 404 error if the profile was not found.
        """
        updated_rows = ProfileMapper.update_profile(user_id=session.get("user_id"), data=data.get("profile"), db_session=db_session)

        if not updated_rows:
            response_data = {"error": "Profile not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Profile updated", "updated_rows": updated_rows}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def delete_profile(user_id, db_session=None):
        """
        Deletes a profile by its ID.

        Args:
            user_id: The ID of the user associated with the profile to delete.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object with a success message if the profile was deleted, or a 404 error if the profile was not found.
        """
        deleted_rows = ProfileMapper.delete_profile(user_id=user_id, db_session=db_session)

        if not deleted_rows:
            response_data = {"error": "Profile not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Profile deleted", "deleted_rows": deleted_rows}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")

