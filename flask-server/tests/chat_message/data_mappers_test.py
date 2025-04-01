import pytest
from unittest.mock import MagicMock
from datetime import datetime

from app.data_mappers import ChatMessagesMapper


@pytest.fixture
def mock_db_session():
    session = MagicMock()
    session.cursor.return_value = session
    return session


def test_get_messages_by_chat_id(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchall.return_value = [
        {
            "chat_id": 1,
            "message_id": 1,
            "sender_id": 1,
            "message": "hello",
            "sent_at": datetime(2023, 2, 1, 12, 0, 0)
        },
        {
            "chat_id": 1,
            "message_id": 2,
            "sender_id": 1,
            "message": "hello",
            "sent_at": datetime(2023, 2, 1, 12, 0, 0)
        }
    ]

    chat_messages = ChatMessagesMapper.get_messages_by_chat_id(chat_id=1, db_session=mock_db_session)

    assert len(chat_messages) == 2
    assert chat_messages[0]["sender_id"] == 1
    assert chat_messages[1]["sender_id"] == 1
    assert isinstance(chat_messages[0]["sent_at"], datetime)
    assert isinstance(chat_messages[1]["sent_at"], datetime)


def test_get_message_by_id(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.return_value = {
        "chat_id": 1,
        "message_id": 1,
        "sender_id": 1,
        "message": "hello",
        "sent_at": datetime(2023, 2, 1, 12, 0, 0)
    }

    chat_message = ChatMessagesMapper.get_message_by_id(message_id=1, db_session=mock_db_session)

    assert chat_message["chat_id"] == 1
    assert chat_message["message_id"] == 1
    assert isinstance(chat_message["sent_at"], datetime)


def test_create_message(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
        "chat_id": 1,
        "message_id": 1,
        "sender_id": 1,
        "message": "hello",
        "sent_at": datetime(2023, 2, 1, 12, 0, 0)
    }

    chat_id = ChatMessagesMapper.create_message(data=data, db_session=mock_db_session)

    assert chat_id == 3


def test_delete_message(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1

    rows_deleted = ChatMessagesMapper.delete_message(message_id=1, db_session=mock_db_session)

    assert rows_deleted == 1


def test_create_message_missing_fields(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
        "chat_id": 1,
        "message_id": 1,
        "sender_id": 1,
        "message": "hello",
        "sent_at": datetime(2023, 2, 1, 12, 0, 0)
    }

    del data["chat_id"]

    with pytest.raises(expected_exception=TypeError):
        ChatMessagesMapper.create_message(data=data, db_session=mock_db_session)


# noinspection PyDictCreation
def test_create_message_invalid_data_type(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
        "chat_id": 1,
        "message_id": 1,
        "sender_id": 1,
        "message": "hello",
        "sent_at": datetime(2023, 2, 1, 12, 0, 0)
    }

    data["sent_at"] = 2023

    with pytest.raises(expected_exception=TypeError):
        ChatMessagesMapper.create_message(data=data, db_session=mock_db_session)


def test_get_message_by_id_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.side_effect = Exception("Database error")

    with pytest.raises(expected_exception=Exception, match="Database error"):
        ChatMessagesMapper.get_message_by_id(message_id=1, db_session=mock_db_session)


def test_get_messages_by_chat_id_no_results(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchall.return_value = []

    chat_messages = ChatMessagesMapper.get_messages_by_chat_id(chat_id=1, db_session=mock_db_session)

    assert len(chat_messages) == 0


def test_create_message_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.execute.side_effect = Exception("Database error")

    data = {
        "chat_id": 1,
        "message_id": 1,
        "sender_id": 1,
        "message": "hello",
        "sent_at": datetime(2023, 2, 1, 12, 0, 0)
    }

    with pytest.raises(expected_exception=Exception, match="Database error"):
        ChatMessagesMapper.create_message(data=data, db_session=mock_db_session)


def test_delete_message_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.execute.side_effect = Exception("Database error")

    with pytest.raises(expected_exception=Exception, match="Database error"):
        ChatMessagesMapper.delete_message(1, db_session=mock_db_session)
