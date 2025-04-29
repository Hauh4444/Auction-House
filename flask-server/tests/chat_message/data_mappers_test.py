import pytest
from unittest.mock import MagicMock
from datetime import datetime
from app.data_mappers import ChatMessageMapper


@pytest.fixture
def mock_db_session():
    session = MagicMock()
    session.cursor.return_value = session
    return session


def test_get_messages_by_chat_id(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchall.return_value = [
        {
            "message_id": 1,
            "sender_id": 2,
            "chat_id": 3,
            "message": "Hello, world!",
            "sent_at": datetime(2025, 4, 27, 12, 0, 0)
        },
        {
            "message_id": 2,
            "sender_id": 3,
            "chat_id": 3,
            "message": "Hi there!",
            "sent_at": datetime(2025, 4, 27, 12, 5, 0)
        }
    ]

    messages = ChatMessageMapper.get_messages_by_chat_id(chat_id=3, db_session=mock_db_session)

    assert len(messages) == 2
    assert messages[0]["message"] == "Hello, world!"
    assert messages[1]["message"] == "Hi there!"
    assert isinstance(messages[0]["created_at"], datetime)  # Adjusted to 'created_at'
    assert isinstance(messages[1]["created_at"], datetime)  # Adjusted to 'created_at'


def test_get_message_by_id(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.return_value = {
        "message_id": 1,
        "sender_id": 2,
        "chat_id": 3,
        "message": "Hello, world!",
        "sent_at": datetime(2025, 4, 27, 12, 0, 0)
    }

    message = ChatMessageMapper.get_message_by_id(message_id=1, db_session=mock_db_session)

    assert message["message_id"] == 1
    assert message["message"] == "Hello, world!"
    assert isinstance(message["created_at"], datetime)  # Adjusted to 'created_at'


def test_create_message(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
        "sender_id": 2,
        "chat_id": 3,
        "message": "New message",
        "sent_at": datetime(2025, 4, 27, 12, 10, 0)
    }

    message_id = ChatMessageMapper.create_message(data=data, db_session=mock_db_session)

    assert message_id == 3


def test_delete_message(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1

    rows_deleted = ChatMessageMapper.delete_message(message_id=1, db_session=mock_db_session)

    assert rows_deleted == 1


def test_get_message_by_id_not_found(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.return_value = None

    message = ChatMessageMapper.get_message_by_id(message_id=999, db_session=mock_db_session)

    assert message is None
