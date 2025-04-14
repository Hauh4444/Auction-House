from flask import Blueprint, jsonify
from ..utils import logger

# Blueprint for logger-related routes
bp = Blueprint("logger_bp", __name__, url_prefix="/api/logger")

# Initialize logger
app_logger = logger.setup_logger("app_logger", "logs/app.log")


# GET /api/logger/test/
@bp.route("/test/", methods=["GET"])
def log_test_message():
    """
    Logs a test message to verify logging setup.

    Returns:
        Response: A JSON response indicating that a log message was written.
    """
    app_logger.info("Logger test endpoint was accessed.")
    return jsonify({"message": "Test log written to app.log"}), 200
