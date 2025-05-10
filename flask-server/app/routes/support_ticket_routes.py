from flask import Blueprint, request, jsonify, Response
from flask_login import login_required, current_user

from ..services import SupportTicketService
from ..utils.logger import setup_logger

# Blueprint for support ticket routes
bp = Blueprint("support_ticket_bp", __name__, url_prefix="/api/support/tickets")

logger = setup_logger(name="support_ticket_logger", log_file="logs/support_ticket.log")


# GET /api/support/tickets/
@bp.route("/", methods=["GET"])
@login_required
def get_tickets(db_session=None):
    """
    Retrieve all support tickets for the authenticated user.

    Args:
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response containing a list of support tickets.
    """
    return SupportTicketService.get_tickets(db_session=db_session)


# GET /api/support/tickets/{id}/
@bp.route("/<int:ticket_id>/", methods=["GET"])
@login_required
def get_ticket_by_id(ticket_id: int, db_session=None):
    """
    Retrieve details of a specific support ticket.

    Args:
        ticket_id (int): The ID of the support ticket.
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response containing the details of the specified ticket.
    """
    return SupportTicketService.get_ticket_by_id(ticket_id=ticket_id, db_session=db_session)


# POST /api/support/tickets/
@bp.route("/", methods=["POST"])
@login_required
def create_ticket(db_session=None):
    """
    Create a new support ticket.

    Args:
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response containing the newly created ticket details.
    """
    data = request.json
    data.update(user_id=current_user.id, status="Open", priority="Medium", assigned_to=3)
    return SupportTicketService.create_ticket(data=data, db_session=db_session)


# PUT /api/support/tickets/{id}/
@bp.route("/<int:ticket_id>/", methods=["PUT"])
@login_required
def update_ticket(ticket_id: int, db_session=None):
    """
    Update the details of an existing support ticket.

    Args:
        ticket_id (int): The ID of the support ticket.
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response confirming the successful update of the ticket.
    """
    if current_user.role not in ["staff", "admin"]:
        response_data = {"error": "Unauthorized access"}
        logger.error(msg=f"Unauthorized access attempt to update support ticket by user {current_user.id}")
        return Response(response=jsonify(response_data).get_data(), status=401, mimetype="application/json")

    data = request.json
    return SupportTicketService.update_ticket(ticket_id=ticket_id, data=data, db_session=db_session)


# DELETE /api/support/tickets/{id}/
@bp.route("/<int:ticket_id>/", methods=["DELETE"])
@login_required
def delete_ticket(ticket_id: int, db_session=None):
    """
    Delete a support ticket.

    Args:
        ticket_id (int): The ID of the support ticket.
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response confirming the deletion of the ticket.
    """
    if current_user.role not in ["staff", "admin"]:
        response_data = {"error": "Unauthorized access"}
        logger.error(msg=f"Unauthorized access attempt to delete support ticket by user {current_user.id}")
        return Response(response=jsonify(response_data).get_data(), status=401, mimetype="application/json")

    return SupportTicketService.delete_ticket(ticket_id=ticket_id, db_session=db_session)