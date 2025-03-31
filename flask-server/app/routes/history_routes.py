from flask import Blueprint, session, request
from flask_login import login_required

from ..services import HistoryService

# Blueprint for history-related routes
bp = Blueprint("history_bp", __name__, url_prefix="/api/user")


# GET /api/user/orders/
@bp.route('/orders/', methods=['GET'])
@login_required
def get_user_orders(db_session=None):
    """
    Retrieve a user's order history.

    Args:
        db_session (optional): A database session for testing or direct queries.

    Returns:
        JSON response containing a list of the user's past orders.
    """
    data = None
    if session.get("role") in ["staff", "admin"]:
        data = request.json

    return HistoryService.get_user_orders(data=data, db_session=db_session)


# GET /api/user/listings/
@bp.route('/listings/', methods=['GET'])
@login_required
def get_user_listings(db_session=None):
    """
    Retrieve a user's listing history.

    Args:
        db_session (optional): A database session for testing or direct queries.

    Returns:
        JSON response containing a list of the user's past listings.
    """
    data = None
    if session.get("role") in ["staff", "admin"]:
        data = request.json

    return HistoryService.get_user_listings(db_session=db_session)


# GET /api/user/transactions/
@bp.route('/transactions/', methods=['GET'])
@login_required
def get_user_transactions(db_session=None):
    """
    Retrieve a user's transaction history.

    Args:
        db_session (optional): A database session for testing or direct queries.

    Returns:
        JSON response containing a list of the user's past transactions.
    """
    data = None
    if session.get("role") in ["staff", "admin"]:
        data = request.json

    return HistoryService.get_user_transactions(db_session=db_session)


# GET /api/user/deliveries/
@bp.route('/deliveries/', methods=['GET'])
@login_required
def get_user_deliveries(db_session=None):
    """
    Retrieve a user's delivery history.

    Args:
        db_session (optional): A database session for testing or direct queries.

    Returns:
        JSON response containing a list of the user's past deliveries.
    """
    data = None
    if session.get("role") in ["staff", "admin"]:
        data = request.json

    return HistoryService.get_user_deliveries(db_session=db_session)


# GET /api/user/support-tickets/
@bp.route('/support-tickets/', methods=['GET'])
@login_required
def get_user_support_tickets(db_session=None):
    """
    Retrieve a user's support ticket history.

    Args:
        db_session (optional): A database session for testing or direct queries.

    Returns:
        JSON response containing a list of the user's past support tickets.
    """
    data = None
    if session.get("role") in ["staff", "admin"]:
        data = request.json

    return HistoryService.get_user_support_tickets(db_session=db_session)


# GET /api/user/reviews/
@bp.route('/reviews/', methods=['GET'])
@login_required
def get_user_reviews(db_session=None):
    """
    Retrieve a user's review history.

    Args:
        db_session (optional): A database session for testing or direct queries.

    Returns:
        JSON response containing a list of the user's past reviews.
    """
    data = None
    if session.get("role") in ["staff", "admin"]:
        data = request.json
        
    return HistoryService.get_user_reviews(db_session=db_session)
