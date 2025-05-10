import pytest
from datetime import datetime
from app.entities import TicketMessage  # Adjust the import path if necessary


def test_ticket_message_creation():
    ticket_message = TicketMessage(
        ticket_id=123,
        message="This is a test message.",
        sender_id=456
    )

    assert ticket_message.ticket_id == 123
    assert ticket_message.sender_id == 456
    assert ticket_message.message == "This is a test message."
    assert ticket_message.message_id is None
    # sent_at is assigned automatically if not provided
    assert isinstance(ticket_message.sent_at, datetime)


def test_ticket_message_creation_with_sent_at_and_message_id():
    sent_time = datetime(2024, 4, 28, 15, 30, 0)
    ticket_message = TicketMessage(
        ticket_id=789,
        message="Another test message.",
        sender_id=321,
        sent_at=sent_time,
        message_id=101
    )

    assert ticket_message.ticket_id == 789
    assert ticket_message.sender_id == 321
    assert ticket_message.message == "Another test message."
    assert ticket_message.message_id == 101
    assert ticket_message.sent_at == datetime(2024, 4, 28, 15, 30, 0)


def test_ticket_message_to_dict():
    sent_time = datetime(2025, 1, 1, 12, 0, 0)
    ticket_message = TicketMessage(
        ticket_id=555,
        message="Dict test message.",
        sender_id=777,
        sent_at=sent_time,
        message_id=888
    )

    ticket_message_dict = ticket_message.to_dict()

    assert ticket_message_dict["ticket_id"] == 555
    assert ticket_message_dict["sender_id"] == 777
    assert ticket_message_dict["message"] == "Dict test message."
    assert ticket_message_dict["message_id"] == 888
    assert ticket_message_dict["sent_at"] == datetime(2025, 1, 1, 12, 0, 0)


def test_ticket_message_missing_required_fields():
    with pytest.raises(TypeError):
        TicketMessage()


def test_ticket_message_invalid_types():
    with pytest.raises(TypeError):
        TicketMessage(
            ticket_id="invalid",  # Should be int
            message=12345,        # Should be str
            sender_id="invalid"   # Should be int
        )
