from flask import Blueprint, request, jsonify, Response
from flask_login import login_required, current_user

from ..services import TicketMessageService
from ..utils.logger import setup_logger

# Blueprint for ticket message-related routes
bp = Blueprint("ticket_message_bp", __name__, url_prefix="/api/ticket/messages")

logger = setup_logger(name="ticket_message_logger", log_file="logs/ticket_message.log")


# GET /api/ticket/messages/{id}/
@bp.route('/<int:ticket_id>/', methods=['GET'])
@login_required
def get_messages_by_ticket(ticket_id: int, db_session=None):
    """
    Retrieve all messages for a given ticket.

    Args:
        ticket_id (int): The ID of the ticket for which messages are being retrieved.
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response containing the list of messages for the ticket.
    """
    return TicketMessageService.get_messages_by_ticket_id(ticket_id=ticket_id, db_session=db_session)


# POST /api/ticket/messages/{ticket_id}/
@bp.route('/<int:ticket_id>/', methods=['POST'])
@login_required
def create_message(ticket_id: int, db_session=None):
    """
    Create a new message in a support ticket.

    Args:
        ticket_id (int): The ID of the ticket where the message will be added.
        db_session: Optional database session to be used in tests.

    Expects:
        JSON payload containing the message content.

    Returns:
        JSON response indicating the creation status of the message.
    """
    data = request.json
    data.update(sender_id=current_user.id, ticket_id=ticket_id)
    return TicketMessageService.create_message(data=data, db_session=db_session)


# DELETE /api/ticket/messages/{message_id}/
@bp.route('/<int:message_id>/', methods=['DELETE'])
@login_required
def delete_message(message_id: int, db_session=None):
    """
    Delete a ticket message by its ID.

    Args:
        message_id (int): The ID of the message to delete.
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response indicating the status of the deletion.
    """
    if current_user.role not in ["staff", "admin"]:
        response_data = {"error": "Unauthorized access"}
        logger.error(msg=f"Unauthorized access attempt to delete ticket message by user {current_user.id}")
        return Response(response=jsonify(response_data).get_data(), status=401, mimetype="application/json")

    return TicketMessageService.delete_message(message_id=message_id, db_session=db_session)
