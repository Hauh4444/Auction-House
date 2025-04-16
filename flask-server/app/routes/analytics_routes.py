from flask import Blueprint, jsonify, Response
from flask_login import login_required, current_user

from ..services import AnalyticsService

# Blueprint for analytics-related routes
bp = Blueprint("analytics_bp", __name__, url_prefix="/api/analytics")

# GET /api/analytics/login_data/
@bp.route("/login_data/", methods=["GET"])
@login_required
def get_login_data():
    """
    Retrieve login data analytics.

    Returns:
        A base64-encoded image or HTML for the chart
    """
    if current_user.role not in ["staff", "admin"]:
        response_data = {"error": "Unauthorized access"}
        return Response(response=jsonify(response_data).get_data(), status=401, mimetype="application/json")

    return AnalyticsService.get_login_data()