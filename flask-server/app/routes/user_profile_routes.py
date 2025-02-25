from flask import Blueprint, request
from ..services.user_profile_services import UserProfileService

# Blueprint for user profile-related routes
user_profile_bp = Blueprint('user_profile_bp', __name__)


# GET /api/profile/{id}
@user_profile_bp.route('/<int:profile_id>', methods=['GET'])
def get_user_profile_by_id(profile_id):
    """Retrieve user profile information."""
    return UserProfileService.get_user_profile_by_id(profile_id)


# PUT /api/profile
@user_profile_bp.route('/<int:profile_id>', methods=['PUT'])
def update_user_profile(profile_id):
    """Update user profile information."""
    return UserProfileService.update_user_profile(profile_id, request)

# WON'T BE USED YET

# GET /api/profile/orders
@user_profile_bp.route('/orders', methods=['GET'])
def get_user_orders():
    """Retrieve past orders by the user."""
    return UserProfileService.get_user_orders(request)


# GET /api/profile/orders/{id}
@user_profile_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order_details(order_id):
    """Retrieve past order details by order ID."""
    return UserProfileService.get_order_details(order_id)


# GET /api/profile/bids
@user_profile_bp.route('/bids', methods=['GET'])
def get_user_bids():
    """Retrieve past bids by the user."""
    return UserProfileService.get_user_bids(request)


# GET /api/profile/listings
@user_profile_bp.route('/listings', methods=['GET'])
def get_user_listings():
    """Retrieve past listings by the user."""
    return UserProfileService.get_user_listings(request)
