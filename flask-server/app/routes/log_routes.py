from flask import Blueprint, request

from ..services import LogService

bp = Blueprint("log_bp", __name__, url_prefix="/api/logs")


# GET /api/logs/
@bp.route("/", methods=["GET"])
def list_logs():
    return LogService.list_logs()


# GET /api/logs/{filename}/
@bp.route("/<filename>/", methods=["GET"])
def get_log_file(filename):
    args = request.args
    return LogService.get_log_file(filename=filename, args=args)