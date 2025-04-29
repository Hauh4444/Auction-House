import pytest
from unittest.mock import MagicMock

from datetime import datetime

from app.entities import Chat


@pytest.fixture
def mock_db_session():
    session = MagicMock()
    return session


def test_chat_creation():
    chat = Chat(
        user1_id=1,
        user2_id=2
    )

    assert chat.user1_id == 1
    assert chat.user2_id == 2
    assert isinstance(chat.user1_id, int)
    assert isinstance(chat.user2_id, int)
    assert isinstance(chat.created_at, datetime)


def test_chat_with_optional_fields():
    chat = Chat(
        chat_id=1,
        user1_id=1,
        user2_id=2,
        created_at=datetime(2024, 1, 1, 10, 0, 0)
    )

    assert chat.chat_id == 1
    assert chat.created_at == datetime(2024, 1, 1, 10, 0, 0)
    assert isinstance(chat.chat_id, int)
    assert isinstance(chat.created_at, datetime)


def test_chat_to_dict():
    chat = Chat(
        chat_id=1,
        user1_id=1,
        user2_id=2,
        created_at=datetime(2024, 1, 1, 10, 0, 0)
    )

    chat_dict = chat.to_dict()

    assert chat_dict["chat_id"] == 1
    assert chat_dict["user1_id"] == 1
    assert chat_dict["user2_id"] == 2
    assert chat_dict["created_at"] == datetime(2024, 1, 1, 10, 0, 0)
    assert isinstance(chat_dict["chat_id"], int)
    assert isinstance(chat_dict["user1_id"], int)
    assert isinstance(chat_dict["user2_id"], int)
    assert isinstance(chat_dict["created_at"], datetime)


def test_chat_missing_required_fields():
    with pytest.raises(expected_exception=TypeError):
        Chat()


def test_chat_invalid_types():
    with pytest.raises(expected_exception=TypeError):
        Chat(
            chat_id="1",
            user1_id="1",
            user2_id="2",
            created_at=1
        )
