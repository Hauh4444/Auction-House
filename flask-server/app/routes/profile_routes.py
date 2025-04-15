from flask import Blueprint, request
from flask_login import login_required, current_user

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
    if current_user.role in ["staff", "admin"]:
        data = request.args.to_dict()

    return ProfileService.get_profile(data=data, db_session=db_session)


# PUT /api/user/profile/{id}/
@bp.route("/<int:profile_id>/", methods=["PUT"])
@login_required
def update_profile(profile_id, db_session=None):
    """
    Update an existing profile.

    Args:
        profile_id (int): The id of the profile to update
        db_session: Optional database session to be used in tests.

    Returns:
        Response: JSON response with updated profile details.
    """
    data = request.json
    return ProfileService.update_profile(profile_id=profile_id, data=data, db_session=db_session)