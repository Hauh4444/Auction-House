from flask import Blueprint, request
from flask_login import login_required

from ..services import ProfileService

# Blueprint for profile-related routes
bp = Blueprint("profile_bp", __name__, url_prefix="/api/profile")


# GET /api/profile
@bp.route("/", methods=["GET"])
@login_required
def get_all_profiles(db_session=None):
    """Retrieve all profiles.

    Args:
        db_session: Optional database session to be used in tests.

    Returns:
        Response: JSON response with all profiles.
    """
    return ProfileService.get_all_profiles(db_session=db_session)


# GET /api/profile/{id}
@bp.route("/<int:user_id>", methods=["GET"])
@login_required
def get_profile(user_id, db_session=None):
    """Retrieve profile information by user ID.

    Args:
        user_id (int): The unique identifier of the user.
        db_session: Optional database session to be used in tests.

    Returns:
        Response: JSON response containing profile details.
    """
    return ProfileService.get_profile(user_id=user_id, db_session=db_session)


# PUT /api/profile/{id}
@bp.route("/<int:profile_id>", methods=["PUT"])
@login_required
def update_profile(profile_id, db_session=None):
    """Update an existing profile.

    Args:
        profile_id (int): The unique identifier of the profile to be updated.
        db_session: Optional database session to be used in tests.

    Returns:
        Response: JSON response with updated profile details.
    """
    data = request.json["data"]
    return ProfileService.update_profile(profile_id, data=data, db_session=db_session)
