import pytest
from unittest.mock import MagicMock

from datetime import datetime

from app.entities.chat import Chat


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
    assert isinstance(chat.created_at, str)


def test_chat_with_optional_fields():
    chat = Chat(
        user1_id=1,
        user2_id=2,
        created_at=datetime(2024, 1, 1, 10, 0, 0),
        chat_id=1
    )

    assert chat.user1_id == 1
    assert chat.user2_id == 2
    assert chat.created_at == datetime(2024, 1, 1, 10, 0, 0)
    assert chat.chat_id == 1


def test_chat_to_dict():
    chat = Chat(
        user1_id=1,
        user2_id=2
    )

    chat_dict = chat.to_dict()

    assert chat_dict["user1_id"] == 1
    assert chat_dict["user2_id"] == 2
    assert isinstance(chat_dict["created_at"], str)


def test_chat_missing_required_fields():
    with pytest.raises(TypeError):
        Chat()


def test_chat_invalid_types():
    with pytest.raises(TypeError):
        Chat(user1_id="1", user2_id="2")