from flask import jsonify, Response

from ..data_mappers import ChatMessageMapper, ChatMapper
from ..utils.socketio import socketio
from ..utils.logger import setup_logger

logger = setup_logger(name="chat_message_logger", log_file="logs/chat_message.log")


class ChatMessageService:
    @staticmethod
    def get_messages_by_chat_id(chat_id: int, db_session=None):
        """
        Retrieve all messages for a given chat.

        Args:
            chat_id (int): The ID of the chat for which messages are to be retrieved.
            db_session: Optional database session to be used in tests.

        Returns:
            Response: A JSON response containing the chat messages if found, otherwise a 404 error.
        """
        messages = ChatMessageMapper.get_messages_by_chat_id(chat_id=chat_id, db_session=db_session)
        if not messages:
            response_data = {"error": "No messages found"}
            logger.error(msg=f"No messages found for chat: {chat_id}")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Messages found", "messages": messages}
        logger.info(msg=f"Messages found: {[message.get('message') for message in messages]}")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')


    @staticmethod
    def create_message(data: dict, db_session=None):
        """
        Create a new message for a chat.

        Args:
            data (dict): A dictionary containing the message data (e.g., chat_id, message content).
            db_session: Optional database session to be used in tests.

        Returns:
            Response: A JSON response with the success message and message ID, or a 409 error if the message could not be created.
        """
        message_id = ChatMessageMapper.create_message(data=data, db_session=db_session)
        if not message_id:
            response_data = {"error": "Error creating message"}
            logger.error(msg=f"Failed creating message with data: {', '.join(f'{k}={v!r}' for k, v in data.items())}")
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype='application/json')

        updated_rows = ChatMapper.update_chat_timestamp(chat_id=data.get("chat_id"), db_session=db_session)
        if not updated_rows:
            response_data = {"error": "Error updating chat timestamp"}
            logger.error(msg=f"Failed updating timestamp of chat: {data.get('chat_id')}")
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype='application/json')

        socketio.emit("new_message")

        response_data = {"message": "Message created", "message_id": message_id}
        logger.info(msg=f"Message: {message_id} created successfully with data: {', '.join(f'{k}={v!r}' for k, v in data.items())}")
        return Response(response=jsonify(response_data).get_data(), status=201, mimetype='application/json')


    @staticmethod
    def update_message(message_id: int, data: dict, db_session=None):
        """
        Update an existing chat message.

        Args:
            message_id (int): The ID of the message to be updated.
            data (dict): A dictionary containing the updates to be applied to the message.
            db_session: Optional database session to be used in tests.

        Returns:
            Response: A JSON response with a success message if the message was updated, or a 404 error if the message was not found or no changes were made.
        """
        updated_rows = ChatMessageMapper.update_message(message_id=message_id, data=data, db_session=db_session)
        if not updated_rows:
            response_data = {"error": "Error updating chat message"}
            logger.error(msg=f"Failed updating message: {message_id} with data: {', '.join(f'{k}={v!r}' for k, v in data.items())}")
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype='application/json')

        response_data = {"message": "Message updated", "updated_rows": updated_rows}
        logger.info(msg=f"Message: {message_id} updated successfully with data: {', '.join(f'{k}={v!r}' for k, v in data.items())}")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')


    @staticmethod
    def delete_message(message_id: int, db_session=None):
        """
        Delete a chat message by its ID.

        Args:
            message_id (int): The ID of the message to be deleted.
            db_session: Optional database session to be used in tests.

        Returns:
            Response: A JSON response with the success message if the message was deleted, or a 404 error if the message was not found.
        """
        deleted_rows = ChatMessageMapper.delete_message(message_id=message_id, db_session=db_session)
        if not deleted_rows:
            response_data = {"error": "Message not found"}
            logger.error(msg=f"Message: {message_id} not found")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Message deleted", "deleted_rows": deleted_rows}
        logger.info(msg=f"Message: {message_id} deleted successfully")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')
