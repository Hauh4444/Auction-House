from flask import Blueprint, request
from flask_login import login_required

from ..services import AuthService

# Blueprint for user login-related routes
bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")


# GET /api/auth/auth_status - Check authentication status
@bp.route("/auth_status", methods=["GET"])
@login_required
def check_auth_status():
    """Check the authentication status of the current user.

    Returns:
        JSON response indicating whether the user is logged in or not.
    """
    return AuthService.check_auth_status()


# POST /api/auth/register - Register a new user
@bp.route("/register", methods=["POST"])
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
    return AuthService.create_user(data=data, db_session=db_session)


# POST /api/auth/login - Login with username and password
@bp.route("/login", methods=["POST"])
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
    return AuthService.login_user(data=data, db_session=db_session)


# POST /api/auth/logout - Logout of current user
@bp.route("/logout", methods=["POST"])
@login_required
def logout_user():
    """Log out the current user.

    This will invalidate the session or token.

    Returns:
        JSON response indicating the logout status.
    """
    return AuthService.logout_user()


# POST /api/auth/password_reset_request - Request a password reset email
@bp.route("/password_reset_request", methods=["POST"])
@login_required
def password_reset_request():
    """Request a password reset email.

    Expects:
        JSON payload with "email" key.

    Returns:
        JSON response indicating the status of the reset request.
    """
    data = request.json
    return AuthService.password_reset_request(data=data)


# POST /api/auth/password_reset - Reset user password
@bp.route("/password_reset", methods=["POST"])
@login_required
def password_reset(db_session=None):
    """Reset the user password.

    Expects:
        JSON payload with "reset_token" and "new_password" keys.

    Returns:
        JSON response indicating the status of the password reset.
    """
    data = request.json
    return AuthService.reset_user_password(data=data, db_session=db_session)
