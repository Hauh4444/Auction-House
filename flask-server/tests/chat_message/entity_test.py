import pytest
from unittest.mock import MagicMock

from datetime import datetime

from app.entities import ChatMessage


@pytest.fixture
def mock_db_session():
    session = MagicMock()
    return session


def test_chat_message_creation():
    chat_message = ChatMessage(
        sender_id=1,
        chat_id=1,
        message="hello",
    )

    assert chat_message.sender_id == 1
    assert chat_message.chat_id == 1
    assert chat_message.message == "hello"
    assert isinstance(chat_message.sender_id, int)
    assert isinstance(chat_message.chat_id, int)
    assert isinstance(chat_message.message, str)
    assert isinstance(chat_message.sent_at, datetime)



def test_chat_message_with_optional_fields():
    chat_message = ChatMessage(
        message_id=1,
        sender_id=1,
        chat_id=1,
        message="hello",
        sent_at=datetime(2024, 1, 1, 10, 0, 0),
    )

    assert chat_message.message_id == 1
    assert chat_message.sent_at == datetime(2024, 1, 1, 10, 0, 0)
    assert isinstance(chat_message.message_id, int)
    assert isinstance(chat_message.sent_at, datetime)


def test_chat_message_to_dict():
    chat_message = ChatMessage(
        message_id=1,
        sender_id=1,
        chat_id=1,
        message="hello",
        sent_at=datetime(2024, 1, 1, 10, 0, 0),
    )

    chat_message_dict = chat_message.to_dict()

    assert chat_message_dict["message_id"] == 1
    assert chat_message_dict["sender_id"] == 1
    assert chat_message_dict["chat_id"] == 1
    assert chat_message_dict["message"] == "hello"
    assert chat_message_dict["sent_at"] == datetime(2024, 1, 1, 10, 0, 0)  # Adjusted to 'sent_at'




# noinspection PyArgumentList
def test_chat_message_missing_required_fields():
    with pytest.raises(expected_exception=TypeError):
        ChatMessage()


# noinspection PyTypeChecker
def test_chat_message_invalid_types():
    with pytest.raises(expected_exception=TypeError):
        ChatMessage(
            message_id="1",
            sender_id="1",
            chat_id="1",
            message=1,
            sent_at=1,
        )