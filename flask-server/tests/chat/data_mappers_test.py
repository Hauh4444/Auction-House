import pytest
from unittest.mock import MagicMock
from datetime import datetime

from app.data_mappers.chat_mapper import ChatMapper


@pytest.fixture
def mock_db_session():
    session = MagicMock()
    session.cursor.return_value = session
    return session


def test_get_all_chats(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchall.return_value = [
        {
            "chat_id": 1,
            "user1_id": 1,
            "user2_id": 2,
            "created_at": datetime(2023, 1, 1, 12, 0, 0),
        },
        {
            "chat_id": 2,
            "user1_id": 2,
            "user2_id": 3,
            "created_at": datetime(2023, 2, 1, 12, 0, 0),
        }
    ]

    chats = ChatMapper.get_all_chats(db_session=mock_db_session)

    assert len(chats) == 2
    assert chats[0]["user1_id"] == 1
    assert isinstance(chats[0]["created_at"], datetime)


def test_get_chat_by_id(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.return_value = {
        "chat_id": 1,
        "user1_id": 1,
        "user2_id": 2,
        "created_at": datetime(2023, 1, 1, 12, 0, 0),
    }

    chat = ChatMapper.get_chat_by_id(1, db_session=mock_db_session)

    assert chat["chat_id"] == 1
    assert chat["user1_id"] == 1
    assert isinstance(chat["created_at"], datetime)


def test_create_chat(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
        "user1_id": 1,
        "user2_id": 2,
        "created_at": datetime(2023, 3, 1, 12, 0, 0),
    }

    chat_id = ChatMapper.create_chat(data, db_session=mock_db_session)

    assert chat_id == 3


def test_delete_chat(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1

    rows_deleted = ChatMapper.delete_chat(1, db_session=mock_db_session)

    assert rows_deleted == 1


# Test for missing required fields when creating a chat
def test_create_chat_missing_fields(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
        "user1_id": 1,
        "user2_id": 2,
        "created_at": datetime(2023, 3, 1, 12, 0, 0),
    }

    # Missing user1_id (required field)
    del data["user1_id"]

    with pytest.raises(TypeError):
        ChatMapper.create_chat(data, db_session=mock_db_session)


# Test for invalid data types when creating a chat
def test_create_chat_invalid_data_type(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
        "user1_id": 1,
        "user2_id": 2,
        "created_at": datetime(2023, 3, 1, 12, 0, 0),
    }

    # Invalid type for created_at, should be datetime
    data["created_at"] = 2023

    with pytest.raises(TypeError):
        ChatMapper.create_chat(data, db_session=mock_db_session)


# Test for database failure when fetching chat by id
def test_get_chat_by_id_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        ChatMapper.get_chat_by_id(1, db_session=mock_db_session)


# Test for no chats returned when fetching all chats
def test_get_all_chats_no_results(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchall.return_value = []

    chats = ChatMapper.get_all_chats(db_session=mock_db_session)

    assert len(chats) == 0


# Test for database failure when creating a chat
def test_create_chat_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.execute.side_effect = Exception("Database error")

    data = {
        "user1_id": 1,
        "user2_id": 2,
        "created_at": datetime(2023, 3, 1, 12, 0, 0),
    }

    with pytest.raises(Exception, match="Database error"):
        ChatMapper.create_chat(data, db_session=mock_db_session)


# Test for database failure when deleting a chat
def test_delete_chat_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.execute.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        ChatMapper.delete_chat(1, db_session=mock_db_session)
