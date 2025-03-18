from flask import Blueprint
from flask_login import login_required

from ..services import HistoryService

# Blueprint for history-related routes
bp = Blueprint("history_bp", __name__, url_prefix="/api/user/<int:user_id>")


# GET /api/user/{id}/orders
@bp.route('/orders', methods=['GET'])
@login_required
def get_user_orders(user_id, db_session=None):
    """
    Retrieve a single category by its ID.

    Args:
        user_id (int): The ID of the user to retrieve history of.
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response containing category details.
    """
    return HistoryService.get_user_orders(user_id=user_id, db_session=db_session)


# GET /api/user/{id}/listings
@bp.route('/listings', methods=['GET'])
@login_required
def get_user_listings(user_id, db_session=None):
    """
    Retrieve a user's previous listings."""
    return HistoryService.get_user_listings(user_id=user_id, db_session=db_session)


# GET /api/user/{id}/transactions
@bp.route('/transactions', methods=['GET'])
@login_required
def get_user_transactions(user_id, db_session=None):
    """
    Retrieve a user's previous transactions."""
    return HistoryService.get_user_transactions(user_id, db_session=db_session)


# GET /api/user/{id}/deliveries
@bp.route('/deliveries', methods=['GET'])
@login_required
def get_user_deliveries(user_id, db_session=None):
    """
    Retrieve a user's previous deliveries."""
    return HistoryService.get_user_deliveries(user_id, db_session=db_session)


# GET /api/user/{id}/support-tickets
@bp.route('/support-tickets', methods=['GET'])
@login_required
def get_user_support_tickets(user_id, db_session=None):
    """
    Retrieve a user's previous support tickets."""
    return HistoryService.get_user_support_tickets(user_id, db_session=db_session)


# GET /api/user/{id}/reviews
@bp.route('/reviews', methods=['GET'])
@login_required
def get_user_reviews(user_id, db_session=None):
    """
    Retrieve a user's previous reviews."""
    return HistoryService.get_user_reviews(user_id, db_session=db_session)
