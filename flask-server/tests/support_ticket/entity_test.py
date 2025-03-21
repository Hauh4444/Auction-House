import pytest
from datetime import datetime
from app.entities import SupportTicket

def test_support_ticket_creation():
    ticket = SupportTicket(
        user_id=1,
        order_id=101,
        subject="Order not received",
        status="Open",
        priority="High"
    )
    
    assert ticket.user_id == 1
    assert ticket.order_id == 101
    assert ticket.subject == "Order not received"
    assert ticket.status == "Open"
    assert ticket.priority == "High"
    assert isinstance(ticket.created_at, datetime)
    assert isinstance(ticket.updated_at, datetime)

def test_support_ticket_with_optional_fields():
    ticket = SupportTicket(
        ticket_id=10,
        user_id=2,
        order_id=202,
        subject="Damaged item",
        status="In Progress",
        priority="Medium",
        assigned_to=5,
        created_at=datetime(2024, 3, 18, 10, 0, 0),
        updated_at=datetime(2024, 3, 18, 12, 0, 0)
    )
    
    assert ticket.ticket_id == 10
    assert ticket.assigned_to == 5
    assert ticket.created_at == datetime(2024, 3, 18, 10, 0, 0)
    assert ticket.updated_at == datetime(2024, 3, 18, 12, 0, 0)

def test_support_ticket_to_dict():
    ticket = SupportTicket(
        ticket_id=7,
        user_id=3,
        order_id=303,
        subject="Refund request",
        status="Closed",
        priority="Low"
    )
    
    ticket_dict = ticket.to_dict()
    
    assert ticket_dict["ticket_id"] == 7
    assert ticket_dict["user_id"] == 3
    assert ticket_dict["order_id"] == 303
    assert ticket_dict["subject"] == "Refund request"
    assert ticket_dict["status"] == "Closed"
    assert ticket_dict["priority"] == "Low"
"""
def test_support_ticket_missing_required_fields():
    with pytest.raises(TypeError):
        SupportTicket()

def test_support_ticket_invalid_types():
    with pytest.raises(TypeError):
        SupportTicket(
            ticket_id="10",
            user_id="user",
            order_id="order",
            subject=123,
            status=456,
            priority=789,
            assigned_to="staff"
        )
"""