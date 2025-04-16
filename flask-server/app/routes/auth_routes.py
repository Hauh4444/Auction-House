from flask import Blueprint, request, jsonify
from flask_login import login_required
import os
import json
from datetime import datetime

from ..services import AuthService
from ..services.analytics import parse_log_file, count_logins_by_user, count_failed_logins_by_user, count_logins_by_time

# Blueprint for user login-related routes
bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")

# Path to analytics log file
LOG_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'analytics_login.txt')
ANALYTICS_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'analytics.txt')

def track_login(username, response_code, ip):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "username": username,
        "status": "success" if response_code == 200 else "fail",
        "ip": ip
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


# GET /api/auth/auth_status/
@bp.route("/auth_status/", methods=["GET"])
@login_required
def check_auth_status():
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
    username = data.get("username", "unknown")
    ip = request.remote_addr or "unknown"

    response = AuthService.login(data=data, db_session=db_session)

    try:
        status_code = response[1] if isinstance(response, tuple) else 500
    except Exception:
        status_code = 500
    track_login(username, status_code, ip)

    return response


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


# GET /api/auth/analytics/
@bp.route("/analytics/", methods=["GET"])
@login_required
def login_analytics():
    """
    Fetch login analytics data, such as successful logins by user, failed logins, and logins by hour.
    The results are written to the `analytics.txt` file.
    """
    log_data = parse_log_file()

    login_counts = count_logins_by_user(log_data)
    failed_counts = count_failed_logins_by_user(log_data)
    logins_by_hour = count_logins_by_time(log_data)

    # Writing the analytics data to a file
    with open(ANALYTICS_FILE, "w") as f:
        f.write("Login Analytics\n")
        f.write("====================\n")
        f.write("Successful Logins by User:\n")
        for user, count in login_counts.items():
            f.write(f"{user}: {count} successful logins\n")

        f.write("\nFailed Logins by User:\n")
        for user, count in failed_counts.items():
            f.write(f"{user}: {count} failed logins\n")

        f.write("\nLogins by Hour:\n")
        for hour, count in logins_by_hour.items():
            f.write(f"{hour}: {count} logins\n")

    return jsonify({"message": "Analytics data written to analytics.txt"})
