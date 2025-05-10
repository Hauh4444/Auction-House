from flask import Blueprint, request, jsonify, Response
from flask_login import current_user

from ..services import LogService
from ..utils.logger import setup_logger

# Blueprint for log-related routes
bp = Blueprint("log_bp", __name__, url_prefix="/api/logs")

logger = setup_logger(name="log_logger", log_file="logs/log.log")


# GET /api/logs/
@bp.route("/", methods=["GET"])
def list_logs():
    """
    Retrieve a list of available log files.

    Returns:
        Response: JSON response with a list of log filenames and HTTP 200 status code,
                  or an error with HTTP 401 if access is unauthorized.
    """
    if current_user.role != "admin":
        response_data = {"error": "Unauthorized access"}
        logger.error(msg=f"Unauthorized access attempt to get logs by user {current_user.id}")
        return Response(response=jsonify(response_data).get_data(), status=401, mimetype="application/json")

    return LogService.list_logs()


# GET /api/logs/{filename}/
@bp.route("/<filename>/", methods=["GET"])
def get_log_file(filename: str):
    """
    Retrieve the contents of a specific log file, optionally filtered by level and date.

    Args:
        filename (str): Filename of the log to retrieve

    Returns:
        Response: JSON response with filtered log content and HTTP 200 status code,
                  or an error with an appropriate HTTP status code on failure or unauthorized access.
    """
    if current_user.role != "admin":
        response_data = {"error": "Unauthorized access"}
        logger.error(msg=f"Unauthorized access attempt to get log file by user {current_user.id}")
        return Response(response=jsonify(response_data).get_data(), status=401, mimetype="application/json")

    args = request.args
    return LogService.get_log_file(filename=filename, args=args)