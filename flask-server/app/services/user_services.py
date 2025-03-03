from flask import jsonify, Response

from .profile_services import ProfileService
from ..data_mappers import UserMapper


class UserService:
    @staticmethod
    def get_user(user_id, db_session=None):
        """
        Retrieves a user by their ID.

        Args:
            user_id: The ID of the user to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object with the user details if found, otherwise a 404 error with a message.
        """
        user = UserMapper.get_user(user_id=user_id, db_session=db_session)

        if user:
            data = {"message": "User found", "user": user}
            response = Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')
            return response

        data = {"error": "User not found"}
        response = Response(response=jsonify(data).get_data(), status=404, mimetype='application/json')
        return response

    @staticmethod
    def update_user(user_id, data, db_session=None):
        """
        Updates user information.

        Args:
            user_id: The ID of the user to update.
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object indicating success or an error message if the user is not found.
        """
        updated_rows = UserMapper.update_user(user_id=user_id, data=data, db_session=db_session)

        if updated_rows:
            data = {"message": "User updated", "updated_rows": updated_rows}
            response = Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')
            return response

        data = {"error": "User not found"}
        response = Response(response=jsonify(data).get_data(), status=404, mimetype='application/json')
        return response

    @staticmethod
    def delete_user(user_id, db_session=None):
        """
        Deletes a user by their ID.

        Args:
            user_id: The ID of the user to delete.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object with a success message if the user was deleted, or a 404 error if the user was not found.
        """
        ProfileService.delete_profile(user_id=user_id, db_session=db_session)
        deleted_rows = UserMapper.delete_user(user_id=user_id, db_session=db_session)

        if deleted_rows:
            data = {"message": "User deleted", "deleted_rows": deleted_rows}
            response = Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')
            return response

        data = {"error": "User not found"}
        response = Response(response=jsonify(data).get_data(), status=404, mimetype='application/json')
        return response