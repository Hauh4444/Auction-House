from flask import Blueprint, request
from flask_login import login_required

from ..services.user_profile_services import UserProfileService

# Blueprint for user profile-related routes
user_profile_bp = Blueprint('user_profile_bp', __name__)


# GET /api/profile
@user_profile_bp.route('/', methods=['GET'])
@login_required
def get_all_user_profiles():
    """Retrieve all user profiles.

    Returns:
        Response: JSON response with all user profiles.
    """
    return UserProfileService.get_all_user_profiles()


# GET /api/profile/{id}
@user_profile_bp.route('/<int:user_id>', methods=['GET'])
@login_required
def get_user_profile(user_id):
    """Retrieve user profile information by user ID.

    Args:
        user_id (int): The unique identifier of the user.

    Returns:
        Response: JSON response containing user profile details.
    """
    return UserProfileService.get_user_profile(user_id)


# POST /api/profile
@user_profile_bp.route('/', methods=['POST'])
def create_user_profile():
    """Create a new user profile.

    Expects:
        JSON payload with user profile details.

    Returns:
        Response: JSON response containing the newly created user profile.
    """
    return UserProfileService.create_user_profile(request)


# PUT /api/profile/{id}
@user_profile_bp.route('/<int:profile_id>', methods=['PUT'])
@login_required
def update_user_profile(profile_id):
    """Update an existing user profile.

    Args:
        profile_id (int): The unique identifier of the user profile to be updated.

    Returns:
        Response: JSON response with updated profile details.
    """
    return UserProfileService.update_user_profile(profile_id, request)
