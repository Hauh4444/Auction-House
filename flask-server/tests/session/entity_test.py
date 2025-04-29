import pytest
from datetime import datetime, timedelta
from app.entities import Session

def test_session_creation():
    session = Session(
        user_id=1,
        role="admin",
        token="abcdef123456",
        expires_at=datetime(2024, 3, 20, 12, 0, 0)
    )
    
    assert session.user_id == 1
    assert session.role == "admin"
    assert session.token == "abcdef123456"
    assert session.expires_at == datetime(2024, 3, 20, 12, 0, 0)
    assert isinstance(session.created_at, datetime)

def test_session_with_optional_fields():
    session = Session(
        session_id=10,
        user_id=2,
        role="user",
        token="xyz789",
        expires_at=datetime(2024, 3, 25, 14, 0, 0),
        created_at=datetime(2024, 3, 18, 10, 0, 0)
    )
    
    assert session.session_id == 10
    assert session.created_at == datetime(2024, 3, 18, 10, 0, 0)
    assert session.expires_at == datetime(2024, 3, 25, 14, 0, 0)

def test_session_to_dict():
    session = Session(
        session_id=5,
        user_id=3,
        role="moderator",
        token="modtoken123",
        expires_at=datetime(2024, 3, 22, 16, 0, 0)
    )
    
    session_dict = session.to_dict()
    
    assert session_dict["session_id"] == 5
    assert session_dict["user_id"] == 3
    assert session_dict["role"] == "moderator"
    assert session_dict["token"] == "modtoken123"
    assert session_dict["expires_at"] == datetime(2024, 3, 22, 16, 0, 0)
"""
def test_session_missing_required_fields():
    with pytest.raises(TypeError):
        Session()

def test_session_invalid_types():
    with pytest.raises(TypeError):
        Session(
            session_id="10",
            user_id="user",
            role=123,
            token=456,
            expires_at="invalid_date"
        )
"""