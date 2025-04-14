
from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime

class EventLog(Base):
    __tablename__ = 'event_logs'

    id = Column(Integer, primary_key=True)
    event_name = Column(String, nullable=False)
    user_id = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(JSON)
