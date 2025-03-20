from flask import Blueprint, request
from flask_login import login_required

from ..services import UserService

# Blueprint for user login-related routes
bp = Blueprint("user_bp", __name__, url_prefix="/api/user")


# GET /api/user/
@bp.route("/", methods=["GET"])
@login_required
def get_user(db_session=None):
    """
    Get the details of the currently logged-in user.

    Args:
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response with user details.
    """
    return UserService.get_user(db_session=db_session)


# PUT /api/user/
@bp.route("/", methods=["PUT"])
@login_required
def update_user(db_session=None):
    """
    Updates a user.

    Args:
        db_session: Optional database session to be used in tests.

    Expects:
        JSON payload with updated profile details.

    Returns:
        JSON response indicating the updated profile.
    """
    data = request.json
    return UserService.update_user(data=data, db_session=db_session)


# DELETE /api/user/
@bp.route("/", methods=["DELETE"])
@login_required
def delete_user(db_session=None):
    """
    Delete the user login credentials and profile.

    Args:
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response indicating the deletion status.
    """
    return UserService.delete_user(db_session=db_session)