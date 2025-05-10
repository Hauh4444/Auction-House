import pytest
from unittest.mock import MagicMock
from datetime import datetime
from app.data_mappers import TicketMessageMapper


@pytest.fixture
def mock_db_session():
    session = MagicMock()
    session.cursor.return_value = session
    return session


def test_get_messages_by_ticket_id(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchall.return_value = [
        {
            "message_id": 1,
            "sender_id": 2,
            "ticket_id": 3,
            "message": "Hello, world!",
            "sent_at": datetime(2025, 4, 27, 12, 0, 0)
        },
        {
            "message_id": 2,
            "sender_id": 3,
            "ticket_id": 3,
            "message": "Hi there!",
            "sent_at": datetime(2025, 4, 27, 12, 5, 0)
        }
    ]

    messages = TicketMessageMapper.get_messages_by_ticket_id(ticket_id=3, db_session=mock_db_session)

    assert len(messages) == 2
    assert messages[0]["message"] == "Hello, world!"
    assert messages[1]["message"] == "Hi there!"
    assert isinstance(messages[0]["sent_at"], datetime)  # Adjusted to 'sent_at'
    assert isinstance(messages[1]["sent_at"], datetime)  # Adjusted to 'sent_at'


def test_create_message(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
        "sender_id": 2,
        "ticket_id": 3,
        "message": "New message",
        "sent_at": datetime(2025, 4, 27, 12, 10, 0)
    }

    message_id = TicketMessageMapper.create_message(data=data, db_session=mock_db_session)

    assert message_id == 3


def test_delete_message(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1

    rows_deleted = TicketMessageMapper.delete_message(message_id=1, db_session=mock_db_session)

    assert rows_deleted == 1

