from flask import jsonify, Response, session

from ..data_mappers import ChatMessageMapper, ChatMapper
from ..utils.logger import setup_logger

message_logger = setup_logger("message", "logs/message.log")


class ChatMessageService:
    @staticmethod
    def get_messages_by_chat_id(chat_id, db_session=None):
        """
        Retrieve all messages for a given chat.

        Args:
            chat_id (int): The ID of the chat for which messages are to be retrieved.
            db_session (Session, optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response containing the chat messages if found, otherwise a 404 error.
        """
        messages = ChatMessageMapper.get_messages_by_chat_id(chat_id=chat_id, db_session=db_session)

        if not messages:
            response_data = {"error": "No messages found for this chat"}
            message_logger.error("No messages found for chat id " + chat_id)
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Messages found", "messages": messages}
        message_logger.info("Successfully got message: " + chat_id)
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')


    @staticmethod
    def create_message(data, db_session=None):
        """
        Create a new message for a chat.

        Args:
            data (dict): A dictionary containing the message data (e.g., chat_id, message content).
            db_session (Session, optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response with the success message and message ID, or a 409 error if the message could not be created.
        """
        message_id = ChatMessageMapper.create_message(data=data, db_session=db_session)

        if not message_id:
            response_data = {"error": "Error creating message"}
            message_logger.error("Failed to create message")
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype='application/json')

        updated_rows = ChatMapper.update_chat_timestamp(chat_id=data.get("chat_id"), db_session=db_session)

        if not updated_rows:
            response_data = {"error": "Error updating chat timestamp"}
            message_logger.error("Failed to update chat timestamp")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Message created", "message_id": message_id}
        message_logger.info("Message successfully created with id " + message_id)
        return Response(response=jsonify(response_data).get_data(), status=201, mimetype='application/json')


    @staticmethod
    def update_message(message_id, data, db_session=None):
        """
        Update an existing chat message.

        Args:
            message_id (int): The ID of the message to be updated.
            data (dict): A dictionary containing the updates to be applied to the message.
            db_session (Session, optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response with a success message if the message was updated, or a 404 error if the message was not found or no changes were made.
        """
        updated_rows = ChatMessageMapper.update_message(message_id=message_id, data=data, db_session=db_session)

        if not updated_rows:
            response_data = {"error": "Message not found or no changes made"}
            message_logger.error("Failed to update message " + message_id)
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Message updated", "updated_rows": updated_rows}
        message_logger.info("Successfully updated message " + message_id)
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')


    @staticmethod
    def delete_message(message_id, db_session=None):
        """
        Delete a chat message by its ID.

        Args:
            message_id (int): The ID of the message to be deleted.
            db_session (Session, optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response with the success message if the message was deleted, or a 404 error if the message was not found.
        """
        deleted_rows = ChatMessageMapper.delete_message(message_id=message_id, db_session=db_session)

        if not deleted_rows:
            response_data = {"error": "Message not found"}
            message_logger.error("Failed to delete. Message not found.")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Message deleted", "deleted_rows": deleted_rows}
        message_logger.info("Message with id " + message_id + " successfully deleted")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')
