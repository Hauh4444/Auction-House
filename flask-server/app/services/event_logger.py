from app.models.event_log import EventLog
from app.database import db_session

def log_event(event_name, user_id="anonymous", details=None):
    event = EventLog(
        event_name=event_name,
        user_id=user_id,
        details=details or {}
    )
    db_session.add(event)
    db_session.commit()