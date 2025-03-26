from flask import Blueprint, request, session
from flask_login import login_required

from ..services import ProfileService

# Blueprint for profile-related routes
bp = Blueprint("profile_bp", __name__, url_prefix="/api/user/profile")


# GET /api/user/profile/
@bp.route("/", methods=["GET"])
@login_required
def get_profile(db_session=None):
    """
    Retrieve profile information by user ID.

    Args:
        db_session: Optional database session to be used in tests.

    Returns:
        Response: JSON response containing profile details.
    """
    data = None
    if session.get("role") in ["staff", "admin"]:
        user_id = request.json.get("user_id")
        if not user_id:
            return {"error": "User ID is required for staff"}, 400
        data["user_id"] = user_id
    else:
        data["user_id"] = session.get("user_id")

    return ProfileService.get_profile(data=data, db_session=db_session)


# PUT /api/user/profile/
@bp.route("/", methods=["PUT"])
@login_required
def update_profile(db_session=None):
    """
    Update an existing profile.

    Args:
        db_session: Optional database session to be used in tests.

    Returns:
        Response: JSON response with updated profile details.
    """
    data = request.json
    return ProfileService.update_profile(data=data, db_session=db_session)
