import pytest
from unittest.mock import MagicMock
from datetime import datetime

from app.data_mappers import SessionMapper


@pytest.fixture
def mock_db_session():
    session = MagicMock()
    session.cursor.return_value = session
    return session


def test_get_all_sessions(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchall.return_value = [
        {
            "session_id": 1, "user_id": 10, "role": "admin", "token": "abc123",
            "created_at": datetime(2024, 1, 1), "expires_at": datetime(2024, 1, 3)
        },
        {
            "session_id": 2, "user_id": 11, "role": "user", "token": "xyz789",
            "created_at": datetime(2024, 2, 1), "expires_at": datetime(2024, 2, 3)
        }
    ]
    
    sessions = SessionMapper.get_all_sessions(db_session=mock_db_session)
    
    assert len(sessions) == 2
    assert sessions[0]["role"] == "admin"
    assert sessions[1]["role"] == "user"
    assert isinstance(sessions[0]["created_at"], datetime)


def test_get_session_by_id(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.return_value = {
        "session_id": 1, "user_id": 10, "role": "admin", "token": "abc123",
        "created_at": datetime(2024, 1, 1), "expires_at": datetime(2024, 1, 3)
    }

    session = SessionMapper.get_session_by_id(session_id=1, db_session=mock_db_session)

    assert session["session_id"] == 1
    assert session["role"] == "admin"


def test_create_session(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
        "user_id": 12, "role": "guest", "token": "guest456",
        "created_at": datetime(2025, 3, 3), "expires_at": datetime(2025, 3, 5)
    }

    created_session = SessionMapper.create_session(data=data, db_session=mock_db_session)

    assert created_session == 3


def test_update_session(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1
    data = {
        "role": "moderator",
        "token": "newtoken123",
        "user_id": 1,
        "expires_at": datetime(2025, 3, 5)
    }

    rows_updated = SessionMapper.update_session(session_id=1, data=data, db_session=mock_db_session)

    assert rows_updated == 1


def test_delete_session(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1

    rows_deleted = SessionMapper.delete_session(session_id=1, db_session=mock_db_session)

    assert rows_deleted == 1

def test_create_session_missing_fields(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
        "user_id": 30, "role": "user", "token": "new_token", 
        "created_at": datetime(2024, 3, 1), "expires_at": datetime(2024, 3, 2)
    }

    del data["token"]

    with pytest.raises(expected_exception=TypeError):
        SessionMapper.create_session(data=data, db_session=mock_db_session)


def test_get_session_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.side_effect = Exception("Database error")

    with pytest.raises(expected_exception=Exception, match="Database error"):
        SessionMapper.get_session_by_id(session_id=1, db_session=mock_db_session)


def test_create_session_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.execute.side_effect = Exception("Database error")
    data = {
        "user_id": 30, "role": "user", "token": "new_token", 
        "created_at": datetime(2024, 3, 1), "expires_at": datetime(2024, 3, 2)
    }

    with pytest.raises(expected_exception=Exception, match="Database error"):
        SessionMapper.create_session(data=data, db_session=mock_db_session)


def test_update_session_invalid_id(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 0  # Simulate no rows were updated

    data = {
        "user_id": 40, "role": "editor", "token": "updated_token", 
        "created_at": datetime(2024, 4, 1), "expires_at": datetime(2024, 4, 2)
    }

    rows_updated = SessionMapper.update_session(session_id=999, data=data, db_session=mock_db_session)  # Invalid ID

    assert rows_updated == 0  # Expecting no rows to be updated


def test_delete_session_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.execute.side_effect = Exception("Database error")

    with pytest.raises(expected_exception=Exception, match="Database error"):
        SessionMapper.delete_session(session_id=1, db_session=mock_db_session)