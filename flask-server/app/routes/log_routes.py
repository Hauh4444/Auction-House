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
    if current_user.role != "admin":
        response_data = {"error": "Unauthorized access"}
        logger.error(msg=f"Unauthorized access attempt to get logs by user {current_user.id}")
        return Response(response=jsonify(response_data).get_data(), status=401, mimetype="application/json")

    return LogService.list_logs()


# GET /api/logs/{filename}/
@bp.route("/<filename>/", methods=["GET"])
def get_log_file(filename):
    if current_user.role != "admin":
        response_data = {"error": "Unauthorized access"}
        logger.error(msg=f"Unauthorized access attempt to get log file by user {current_user.id}")
        return Response(response=jsonify(response_data).get_data(), status=401, mimetype="application/json")

    args = request.args
    return LogService.get_log_file(filename=filename, args=args)