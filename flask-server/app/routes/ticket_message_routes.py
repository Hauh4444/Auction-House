from flask import Blueprint, request, session
from flask_login import login_required, current_user

from ..services import TicketMessageService

# Blueprint for ticket message-related routes
bp = Blueprint("ticket_message_bp", __name__, url_prefix="/api/ticket/messages")


# GET /api/ticket/messages/{ticket_id}/
@bp.route('/<int:ticket_id>/', methods=['GET'])
@login_required
def get_messages_by_ticket(ticket_id, db_session=None):
    """
    Retrieve all messages for a given ticket.
    """
    return TicketMessageService.get_messages_by_ticket_id(ticket_id=ticket_id, db_session=db_session)


# POST /api/ticket/messages/{ticket_id}/
@bp.route('/<int:ticket_id>/', methods=['POST'])
@login_required
def create_message(ticket_id, db_session=None):
    """
    Create a new message in a support ticket.
    """
    data = request.json
    data.update(sender_id=session.get("user_id"), ticket_id=ticket_id)
    print(current_user.user_id)
    return TicketMessageService.create_message(data=data, db_session=db_session)


# PUT /api/ticket/messages/{message_id}/
@bp.route('/<int:message_id>/', methods=['PUT'])
@login_required
def update_message(message_id, db_session=None):
    """
    Update an existing ticket message.
    """
    data = request.json
    return TicketMessageService.update_message(message_id=message_id, updates=data, db_session=db_session)


# DELETE /api/ticket/messages/{message_id}/
@bp.route('/<int:message_id>/', methods=['DELETE'])
@login_required
def delete_message(message_id, db_session=None):
    """
    Delete a ticket message by its ID.
    """
    return TicketMessageService.delete_message(message_id=message_id, db_session=db_session)