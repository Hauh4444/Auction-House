from flask import Blueprint, session
from flask_login import login_required

from ..services import ListService

# Blueprint for list-related routes
bp = Blueprint("list_bp", __name__, url_prefix="/api/user/lists")


# GET /api/user/lists/{id}
@bp.route('/<int:list_id>', methods=['GET'])
@login_required
def get_user_lists(list_id, db_session=None):
    """
    Retrieve a user's list items."""
    return ListService.get_user_lists(list_id=list_id, db_session=db_session)


# GET /api/user/lists
@bp.route('/', methods=['GET'])
@login_required
def get_user_lists(db_session=None):
    """
    Retrieve all user's lists.

    Args:
        db_session: Optional database session to be used in tests.

    Returns:
        Response: JSON response with all profiles.
    """
    user_id = session["user_id"]
    return ListService.get_user_lists(user_id=user_id, db_session=db_session)