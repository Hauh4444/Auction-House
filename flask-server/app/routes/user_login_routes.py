from flask import Blueprint, request, jsonify
from flask_login import login_required
from ..services.user_login_services import UserLoginService

# Blueprint for user login-related routes
user_bp = Blueprint('user_bp', __name__)


# POST /api/user/register - Register a new user
@user_bp.route('/register', methods=['POST'])
def register_user():
    """Register a new user.

    Expects:
        JSON payload with user details (username, password, email, etc.).

    Returns:
        JSON response indicating the registration status.
    """
    return UserLoginService.register_user(request)


# POST /api/user/login - Login with username and password
@user_bp.route('/login', methods=['POST'])
def login_user():
    """Login a user by verifying their username and password.

    Expects:
        JSON payload with "username" and "password" keys.

    Returns:
        JSON response indicating the login status.
    """
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    return UserLoginService.login_user(username, password)


# POST /api/user/logout - Logout of current user
@user_bp.route('/logout', methods=['POST'])
@login_required
def logout_user():
    """Log out the current user.

    This will invalidate the session or token.

    Returns:
        JSON response indicating the logout status.
    """
    return UserLoginService.logout_user()


# POST /api/user/password_reset_request - Request a password reset email
@user_bp.route('/password_reset_request', methods=['POST'])
def password_reset_request():
    """Request a password reset email.

    Expects:
        JSON payload with "email" key.

    Returns:
        JSON response indicating the status of the reset request.
    """
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    return UserLoginService.password_reset_request(email)


# POST /api/user/password_reset - Reset user password
@user_bp.route('/password_reset', methods=['POST'])
def password_reset():
    """Reset the user password.

    Expects:
        JSON payload with "reset_token" and "new_password" keys.

    Returns:
        JSON response indicating the status of the password reset.
    """
    data = request.json
    reset_token = data.get("reset_token")
    new_password = data.get("new_password")

    if not reset_token or not new_password:
        return jsonify({"error": "Reset token and new password are required"}), 400

    return UserLoginService.reset_user_password(reset_token, new_password)


# GET /api/user/{id} - Get user login details
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user_details(user_id):
    """Get the details of the currently logged-in user.

    Returns:
        JSON response with user details.
    """
    return UserLoginService.get_user_by_id(user_id)


# GET /api/user/auth_status - Check authentication status
@user_bp.route('/auth_status', methods=['GET'])
def check_auth_status():
    """Check the authentication status of the current user.

    Returns:
        JSON response indicating whether the user is logged in or not.
    """
    return UserLoginService.check_auth_status()


# DELETE /api/user/{id} - Delete user login credentials and user profile
@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete the user login credentials and user profile.

    Returns:
        JSON response indicating the deletion status.
    """
    return UserLoginService.delete_user(user_id)
