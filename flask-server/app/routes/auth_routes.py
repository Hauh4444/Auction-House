from flask import Blueprint, request, jsonify
from flask_login import login_required
from ..utils import logger

from ..services import AuthService

# Blueprint for user login-related routes
bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")


# GET /api/auth/auth_status/
@bp.route("/auth_status/", methods=["GET"])
@login_required
def check_auth_status():
    auth_logger = logger.setup_logger("auth", "logs/auth.log")
    """
    Check the authentication status of the current user.

    Returns:
        Response: A JSON response indicating whether the user is logged in or not.
    """
    return AuthService.check_auth_status()


# POST /api/auth/register/
@bp.route("/register/", methods=["POST"])
def create_user(db_session=None):
    """
    Register a new user.

    Args:
        db_session (Session, optional): A database session for testing or direct queries.

    Expects:
        JSON payload with user details (e.g., username, password, email, etc.).

    Returns:
        Response: A JSON response indicating the registration status.
    """
    data = request.json
    return AuthService.create_user(data=data, db_session=db_session)


# POST /api/auth/login/
@bp.route("/login/", methods=["POST"])
def login(db_session=None):
    """
    Login a user by verifying their username and password.

    Args:
        db_session (Session, optional): A database session for testing or direct queries.

    Expects:
        JSON payload with "username" and "password" keys.

    Returns:
        Response: A JSON response indicating the login status.
    """
    data = request.json
    return AuthService.login(data=data, db_session=db_session)


# POST /api/auth/logout/
@bp.route("/logout/", methods=["POST"])
@login_required
def logout():
    """
    Log out the current user.

    This will invalidate the session or token.

    Returns:
        Response: A JSON response indicating the logout status.
    """
    return AuthService.logout()


# POST /api/auth/password_reset_request/
@bp.route("/password_reset_request/", methods=["POST"])
@login_required
def password_reset_request(db_session=None):
    """
    Request a password reset email.

    Args:
        db_session (Session, optional): A database session for testing or direct queries.

    Returns:
        Response: A JSON response indicating the status of the reset request.
    """
    return AuthService.password_reset_request(db_session=db_session)


# POST /api/auth/password_reset/
@bp.route("/password_reset/", methods=["POST"])
@login_required
def password_reset(db_session=None):
    """
    Reset the user password.

    Args:
        db_session (Session, optional): A database session for testing or direct queries.

    Expects:
        JSON payload with "reset_token" and "new_password" keys.

    Returns:
        Response: A JSON response indicating the status of the password reset.
    """
    data = request.get_json()
    reset_token = data.get('token')
    new_password = data.get('new_password')
    if not reset_token or not new_password:
        return jsonify({"error": "Token and new password are required"}), 400
    return AuthService.reset_user_password(reset_token=reset_token, new_password=new_password, db_session=db_session)
