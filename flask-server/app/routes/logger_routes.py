import os
from flask import Blueprint, jsonify, send_file, abort
from flask import current_app as app
from flask_login import current_user
from ..utils import logger

# Directory where log files are stored
LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "logs"))

# Blueprint for logger-related routes
bp = Blueprint("logger_bp", __name__, url_prefix="/api/logger")

# Initialize app logger
app_logger = logger.setup_logger("app_logger", os.path.join(LOG_DIR, "app.log"))



# GET /api/logger/logs/
@bp.route("/logs/", methods=["GET"])
def list_log_files():
    try:
        log_files = [f for f in os.listdir(LOG_DIR) if os.path.isfile(os.path.join(LOG_DIR, f))]
        app_logger.info(current_user.id + " successfully pulled the logs")
        return jsonify({"logs": log_files}), 200
    except Exception as e:
        app_logger.error(f"Error listing logs: {e}. Current user: " + current_user.id)
        return jsonify({"error": "Could not retrieve log files"}), 500


# GET /api/logger/logs/<filename>
@bp.route("/logs/<filename>", methods=["GET"])
def get_log_file(filename):
    filepath = os.path.join(LOG_DIR, filename)

    if not os.path.isfile(filepath):
        app_logger.error("Error: log file " + filename + " was not found by user: " + current_user.id)
        return jsonify({"error": "Log file not found"}), 404

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        app_logger.info("Successfully retrieved log " + filename + " by user: " + current_user.id)
        return jsonify({
            "filename": filename,
            "lines": lines
        }), 200
    except Exception as e:
        app_logger.error(f"Error reading log file {filename}: {e}. Current user: " + current_user.id)
        return jsonify({"error": "Could not read log file"}), 500


# DELETE /api/logger/logs/<filename>
@bp.route("/logs/<filename>", methods=["DELETE"])
def delete_log_file(filename):
    filepath = os.path.join(LOG_DIR, filename)
    if not os.path.isfile(filepath):
        app_logger.error("Error: log file " + filename + " was not found by user: " + current_user.id)
        return jsonify({"error": "Log file not found"}), 404
    try:
        os.remove(filepath)
        app_logger.info(f"Successfully deleted log file: {filename} by user: " + current_user.id)
        return jsonify({"message": f"{filename} deleted"}), 200
    except Exception as e:
        app_logger.error(f"Error deleting log file {filename}: {e}. Current user: " + current_user.id)
        return jsonify({"error": "Could not delete log file"}), 500
