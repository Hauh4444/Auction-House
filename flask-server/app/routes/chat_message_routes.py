from flask import Blueprint, request, session
from flask_login import login_required, current_user

from ..services import ChatMessageService

# Blueprint for chat message-related routes
bp = Blueprint("chat_message_bp", __name__, url_prefix="/api/user/messages")


# GET /api/user/messages/{chat_id}/
@bp.route('/<int:chat_id>/', methods=['GET'])
@login_required
def get_messages_by_chat(chat_id, db_session=None):
    """
    Retrieve all messages for a given chat.

    Args:
        chat_id (int): The ID of the chat for which messages are being retrieved.
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response containing the list of messages for the chat.
    """
    return ChatMessageService.get_messages_by_chat_id(chat_id=chat_id, db_session=db_session)


# POST /api/user/messages/{chat_id}/
@bp.route('/<int:chat_id>/', methods=['POST'])
@login_required
def create_message(chat_id, db_session=None):
    """
    Create a new message in a support chat.

    Args:
        chat_id (int): The ID of the chat where the message will be added.
        db_session: Optional database session to be used in tests.

    Expects:
        JSON payload containing the message content.

    Returns:
        JSON response indicating the creation status of the message.
    """
    data = request.json
    data.update(sender_id=session.get("user_id"), chat_id=chat_id)
    return ChatMessageService.create_message(data=data, db_session=db_session)


# PUT /api/user/messages/{message_id}/
@bp.route('/<int:message_id>/', methods=['PUT'])
@login_required
def update_message(message_id, db_session=None):
    """
    Update an existing chat message.

    Args:
        message_id (int): The ID of the message to update.
        db_session: Optional database session to be used in tests.

    Expects:
        JSON payload containing the updates for the message.

    Returns:
        JSON response indicating the status of the message update.
    """
    data = request.json
    return ChatMessageService.update_message(message_id=message_id, data=data, db_session=db_session)


# DELETE /api/user/messages/{message_id}/
@bp.route('/<int:message_id>/', methods=['DELETE'])
@login_required
def delete_message(message_id, db_session=None):
    """
    Delete a chat message by its ID.

    Args:
        message_id (int): The ID of the message to delete.
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response indicating the status of the deletion.
    """
    return ChatMessageService.delete_message(message_id=message_id, db_session=db_session)
