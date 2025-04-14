# app/utils/analytics_logger.py
from app.models.event_log import EventLog
from app.database import db_session
from datetime import datetime

def log_event(event_name, user_id=None, details=None):
    """
    Logs an event to the database for analytics purposes.
    """
    event = EventLog(
        event_name=event_name,
        user_id=user_id,
        timestamp=datetime.utcnow(),
        details=details
    )
    db_session.add(event)
    db_session.commit()
