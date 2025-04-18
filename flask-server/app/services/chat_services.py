from flask import jsonify, Response
from flask_login import current_user

from ..data_mappers import ChatMapper
from ..utils.logger import setup_logger

logger = setup_logger(name="chat_logger", log_file="logs/chat.log")


class ChatService:
    @staticmethod
    def get_chats(db_session=None):
        """
        Fetch all support chats for the authenticated user.

        Args:
            db_session (Session, optional): Database session for executing queries.

        Returns:
            Response: JSON response containing the user's chats if available, otherwise a 404 error.
        """
        chats = ChatMapper.get_chats_by_user_id(user_id=current_user.id, db_session=db_session)
        if not chats:
            response_data = {"error": "No chats found"}
            logger.error(msg=f"No chats found")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Chats retrieved", "chats": chats}
        logger.info(msg=f"Chats found: {[chat.get('chat_id') for chat in chats]}")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')


    @staticmethod
    def get_chat_by_id(chat_id, db_session=None):
        """
        Retrieve details of a specific support chat by ID.

        Args:
            chat_id (int): Unique identifier of the chat.
            db_session (Session, optional): Database session for executing queries.

        Returns:
            Response: JSON response with chat details if found, otherwise a 404 error.
        """
        chat = ChatMapper.get_chat_by_id(chat_id=chat_id, db_session=db_session)
        if not chat:
            response_data = {"error": "Chat not found"}
            logger.error(msg=f"Chat: {chat_id} not found")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Chat retrieved", "chat": chat}
        logger.info(msg=f"Chat: {chat_id} found")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')


    @staticmethod
    def create_chat(data, db_session=None):
        """
        Create a new support chat.

        Args:
            data (dict): Payload containing details for creating the chat.
            db_session (Session, optional): Database session for executing queries.

        Returns:
            Response: JSON response with the created chat ID if successful, otherwise a 409 error.
        """
        chat_id = ChatMapper.create_chat(data=data, db_session=db_session)
        if not chat_id:
            response_data = {"error": "Error creating chat"}
            logger.error(msg=f"Failed creating chat with data: {', '.join(f'{k}={v!r}' for k, v in data.items())}")
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype='application/json')

        response_data = {"message": "Chat and message created", "chat_id": chat_id}
        logger.info(msg=f"Chat: {chat_id} created successfully with data: {', '.join(f'{k}={v!r}' for k, v in data.items())}")
        return Response(response=jsonify(response_data).get_data(), status=201, mimetype='application/json')


    @staticmethod
    def update_chat(chat_id, data, db_session=None):
        """
        Update an existing support chat.

        Args:
            chat_id (int): Unique identifier of the chat to update.
            data (dict): Payload containing updated chat details.
            db_session (Session, optional): Database session for executing queries.

        Returns:
            Response: JSON response confirming update success or a 404 error if the chat is not found.
        """
        updated_rows = ChatMapper.update_chat(chat_id=chat_id, data=data, db_session=db_session)
        if not updated_rows:
            response_data = {"error": "Error updating chat"}
            logger.error(msg=f"Failed updating chat: {chat_id} with data: {', '.join(f'{k}={v!r}' for k, v in data.items())}")
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

        response_data = {"message": "Chat updated", "updated_rows": updated_rows}
        logger.info(msg=f"Chat: {chat_id} updated successfully with data: {', '.join(f'{k}={v!r}' for k, v in data.items())}")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def delete_chat(chat_id, db_session=None):
        """
        Delete a support chat by ID.

        Args:
            chat_id (int): Unique identifier of the chat to delete.
            db_session (Session, optional): Database session for executing queries.

        Returns:
            Response: JSON response confirming deletion success or a 404 error if the chat is not found.
        """
        deleted_rows = ChatMapper.delete_chat(chat_id=chat_id, db_session=db_session)
        if not deleted_rows:
            response_data = {"error": "Chat not found"}
            logger.error(msg=f"Chat: {chat_id} not found")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Chat deleted", "deleted_rows": deleted_rows}
        logger.info(msg=f"Chat: {chat_id} deleted successfully")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")