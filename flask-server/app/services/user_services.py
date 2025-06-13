from flask import jsonify, Response
from flask_login import current_user

from ..data_mappers import UserMapper, ProfileMapper
from ..utils.logger import setup_logger

logger = setup_logger(name="user_logger", log_file="logs/user.log")

class UserService:
    @staticmethod
    def get_user(data=None, db_session=None):
        """
        Retrieves a user by their ID.

        Args:
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object with the user details if found, otherwise a 404 error with a message.
        """
        user_id = data.get("user_id") if current_user.role in ["staff", "admin"] else current_user.id
        user = UserMapper.get_user(user_id=user_id, db_session=db_session)

        if not user:
            response_data = {"error": "User not found"}
            logger.error(msg=f"User: {user_id} not found")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "User found", "user": user}
        logger.error(msg=f"User: {user_id} found")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")



    @staticmethod
    def update_user(user_id: int, data: dict, db_session=None):
        """
        Updates user information.

        Args:
            user_id (int): The id of the user to update
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object indicating success or an error message if the user is not found.
        """
        user_id = user_id if current_user.role in ["staff", "admin"] else current_user.id
        updated_rows = UserMapper.update_user(user_id=user_id, data=data, db_session=db_session)

        if not updated_rows:
            response_data = {"error": "Error updating user"}
            logger.error(msg=f"Failed updating user: {user_id} with data: {', '.join(f'{k}={v!r}' for k, v in data.items())}")
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

        response_data = {"message": "User updated", "updated_rows": updated_rows}
        logger.info(msg=f"User: {user_id} updated successfully with data: {', '.join(f'{k}={v!r}' for k, v in data.items())}")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")



    @staticmethod
    def delete_user(user_id: int, db_session=None):
        """
        Deletes a user by their ID.

        Args:
            user_id (int): The id of the user to delete
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object with a success message if the user was deleted, or a 404 error if the user was not found.
        """
        user_id = user_id if current_user.role in ["staff", "admin"] else current_user.id
        deleted_rows = ProfileMapper.delete_profile(user_id=user_id, db_session=db_session)

        if not deleted_rows:
            response_data = {"error": "Profile not found"}
            logger.error(msg=f"Profile not found for user: {user_id}")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        user_id = user_id if current_user.role in ["staff", "admin"] else current_user.id
        deleted_rows = UserMapper.delete_user(user_id=user_id, db_session=db_session)

        if not deleted_rows:
            response_data = {"error": "User not found"}
            logger.error(msg=f"User: {user_id} not found")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "User and profile deleted", "deleted_rows": deleted_rows}
        logger.info(msg=f"User: {user_id} deleted successfully")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")