from flask import Blueprint, request
from flask_login import login_required

from ..services import ChatService

# Blueprint for chat routes
bp = Blueprint("user_chat_bp", __name__, url_prefix="/api/user/chats")


# GET /api/user/chats/
@bp.route("/", methods=["GET"])
@login_required
def get_chats(db_session=None):
    """
    Retrieve all chats for the authenticated user.

    Args:
        db_session (optional): A database session for testing or direct queries.

    Returns:
        JSON response containing a list of chats.
    """
    return ChatService.get_chats(db_session=db_session)


# GET /api/user/chats/{id}/
@bp.route("/<int:chat_id>/", methods=["GET"])
@login_required
def get_chat_by_id(chat_id, db_session=None):
    """
    Retrieve details of a specific chat.

    Args:
        chat_id (int): The ID of the chat.
        db_session (optional): A database session for testing or direct queries.

    Returns:
        JSON response containing the details of the specified chat.
    """
    return ChatService.get_chat_by_id(chat_id=chat_id, db_session=db_session)


# POST /api/user/chats/
@bp.route("/", methods=["POST"])
@login_required
def create_chat(db_session=None):
    """
    Create a new chat.

    Args:
        db_session (optional): A database session for testing or direct queries.

    Returns:
        JSON response containing the newly created chat details.
    """
    data = request.json
    return ChatService.create_chat(data=data, db_session=db_session)


# PUT /api/user/chats/{id}/
@bp.route("/<int:chat_id>/", methods=["PUT"])
@login_required
def update_chat(chat_id, db_session=None):
    """
    Update the details of an existing chat.

    Args:
        chat_id (int): The ID of the chat.
        db_session (optional): A database session for testing or direct queries.

    Returns:
        JSON response confirming the successful update of the chat.
    """
    data = request.json
    return ChatService.update_chat(chat_id=chat_id, data=data, db_session=db_session)


# DELETE /api/user/chats/{id}/
@bp.route("/<int:chat_id>/", methods=["DELETE"])
@login_required
def delete_chat(chat_id, db_session=None):
    """
    Delete a chat.

    Args:
        chat_id (int): The ID of the chat.
        db_session (optional): A database session for testing or direct queries.

    Returns:
        JSON response confirming the deletion of the chat.
    """
    return ChatService.delete_chat(chat_id=chat_id, db_session=db_session)