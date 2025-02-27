from flask import Blueprint, request, jsonify
from flask_login import login_required

from ..services.auth_services import AuthService

# Blueprint for user login-related routes
auth_bp = Blueprint('auth_bp', __name__)


# GET /api/auth/auth_status - Check authentication status
@auth_bp.route('/auth_status', methods=['GET'])
@login_required
def check_auth_status():
    """Check the authentication status of the current user.

    Returns:
        JSON response indicating whether the user is logged in or not.
    """
    return AuthService.check_auth_status()


# POST /api/auth/register - Register a new user
@auth_bp.route('/register', methods=['POST'])
def create_user(db_session=None):
    """Register a new user.

    Args:
        db_session: Optional database session to be used in tests.

    Expects:
        JSON payload with user details (username, password, email, etc.).

    Returns:
        JSON response indicating the registration status.
    """
    data = request.json
    return AuthService.create_user(data, db_session=db_session)


# POST /api/auth/login - Login with username and password
@auth_bp.route('/login', methods=['POST'])
def login_user(db_session=None):
    """Login a user by verifying their username and password.

    Args:
        db_session: Optional database session to be used in tests.

    Expects:
        JSON payload with "username" and "password" keys.

    Returns:
        JSON response indicating the login status.
    """
    data = request.json
    if not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password are required"}), 400
    return AuthService.login_user(data.get("username"), data.get("password"), db_session=db_session)


# POST /api/auth/logout - Logout of current user
@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout_user():
    """Log out the current user.

    This will invalidate the session or token.

    Returns:
        JSON response indicating the logout status.
    """
    return AuthService.logout_user()


# POST /api/auth/password_reset_request - Request a password reset email
@auth_bp.route('/password_reset_request', methods=['POST'])
@login_required
def password_reset_request():
    """Request a password reset email.

    Expects:
        JSON payload with "email" key.

    Returns:
        JSON response indicating the status of the reset request.
    """
    data = request.json
    if not data.get("email"):
        return jsonify({"error": "Email is required"}), 400
    return AuthService.password_reset_request(data.get("email"))


# POST /api/auth/password_reset - Reset user password
@auth_bp.route('/password_reset', methods=['POST'])
@login_required
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
    return AuthService.reset_user_password(reset_token, new_password)
