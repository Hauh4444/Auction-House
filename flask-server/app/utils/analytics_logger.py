from app.models.event_log import EventLog
from app.database import db_session
from datetime import datetime

def log_event(event_name, user_id=None, details=None):
    """
    Logs an event to the database.
    
    Args:
        event_name (str): The name of the event (e.g., 'login', 'bid_add', etc.).
        user_id (str, optional): The ID of the user performing the action.
        details (dict, optional): Additional details about the event (e.g., item listed, bid raised).
    """
    event = EventLog(
        event_name=event_name,
        user_id=user_id,
        timestamp=datetime.utcnow(),
        details=details
    )
    db_session.add(event)
    db_session.commit()
