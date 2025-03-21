import pytest
from datetime import datetime
from app.entities import TicketMessage

def test_ticket_message_creation():
    message = TicketMessage(
        ticket_id=1,
        message="Hello, I need help with my order."
    )
    
    assert message.ticket_id == 1
    assert message.message == "Hello, I need help with my order."
    assert isinstance(message.sent_at, datetime)

def test_ticket_message_with_optional_fields():
    message = TicketMessage(
        message_id=10,
        ticket_id=2,
        user_sender_id=5,
        staff_sender_id=None,
        message="Can you provide an update?",
        sent_at=datetime(2024, 3, 18, 10, 0, 0)
    )
    
    assert message.message_id == 10
    assert message.user_sender_id == 5
    assert message.staff_sender_id is None
    assert message.sent_at == datetime(2024, 3, 18, 10, 0, 0)

def test_ticket_message_to_dict():
    message = TicketMessage(
        message_id=7,
        ticket_id=3,
        user_sender_id=4,
        message="This issue is urgent!"
    )
    
    message_dict = message.to_dict()
    
    assert message_dict["message_id"] == 7
    assert message_dict["ticket_id"] == 3
    assert message_dict["user_sender_id"] == 4
    assert message_dict["staff_sender_id"] is None
    assert message_dict["message"] == "This issue is urgent!"
"""
def test_ticket_message_missing_required_fields():
    with pytest.raises(TypeError):
        TicketMessage()

def test_ticket_message_invalid_types():
    with pytest.raises(TypeError):
        TicketMessage(
            message_id="10",
            ticket_id="ticket",
            user_sender_id="user",
            staff_sender_id="staff",
            message=123
        )
"""