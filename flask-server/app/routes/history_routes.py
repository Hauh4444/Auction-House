from flask import Blueprint
from flask_login import login_required

from ..services import HistoryService

# Blueprint for history-related routes
bp = Blueprint("history_bp", __name__, url_prefix="/api/user/<int:id>")

# TODO: GET /api/user/<int:id>/history          for full user history
#       GET /api/user/<int:id>/orders           for user's previous orders
#       GET /api/user/<int:id>/listings         for user's previous listings
#       GET /api/user/<int:id>/transactions     for user's previous transactions
#       GET /api/user/<int:id>/deliveries       for user's previous deliveries
#       GET /api/user/<int:id>/support-tickets  for user's previous support-tickets
#       GET /api/user/<int:id>/reviews          for user's previous reviews
#       Others will be needed but these are simply a couple examples to show what the routes will look like
#       Routes should all be preceded with the @login_required decorator



# GET /api/user/{id}/orders
@bp.route("/orders", methods=["GET"])
@login_required
def get_user_orders(user_id, db_session=None):
    """Retrieve a single category by its ID.

    Args:
        user_id (int): The ID of the user to retrieve history of.
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response containing category details.
    """
    return HistoryService.get_user_orders(user_id=user_id, db_session=db_session)

