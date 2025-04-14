# FILE: app/routes/analytics_routes.py

from flask import Blueprint, render_template
from app.models.event_log import EventLog
from app.database import db_session

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/analytics")
def analytics_dashboard():
    logs = db_session.query(EventLog).order_by(EventLog.timestamp.desc()).limit(100).all()
    return render_template("analytics.html", logs=logs)
