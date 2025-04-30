import pytest
from datetime import datetime
from app.entities import SupportTicket


def test_support_ticket_creation():
    ticket = SupportTicket(
        user_id=1,
        subject="Order not received",
        status="Open",
        priority="High"
    )
    
    assert ticket.user_id == 1
    assert ticket.subject == "Order not received"
    assert ticket.status == "Open"
    assert ticket.priority == "High"
    assert isinstance(ticket.created_at, datetime)  
    assert isinstance(ticket.updated_at, datetime)  


def test_support_ticket_with_optional_fields():
    created = datetime(2024, 3, 18, 10, 0, 0)
    updated = datetime(2024, 3, 18, 12, 0, 0)

    ticket = SupportTicket(
        ticket_id=10,
        user_id=2,
        subject="Damaged item",
        status="In Progress",
        priority="Medium",
        assigned_to=5,
        created_at=created,
        updated_at=updated
    )
    
    assert ticket.ticket_id == 10
    assert ticket.assigned_to == 5
    assert ticket.created_at == created
    assert ticket.updated_at == updated


def test_support_ticket_to_dict():
    created = datetime(2025, 1, 1, 9, 0, 0)
    updated = datetime(2025, 1, 1, 10, 0, 0)

    ticket = SupportTicket(
        ticket_id=7,
        user_id=3,
        subject="Refund request",
        status="Closed",
        priority="Low",
        created_at=created,
        updated_at=updated
    )
    
    ticket_dict = ticket.to_dict()
    
    assert ticket_dict["ticket_id"] == 7
    assert ticket_dict["user_id"] == 3
    assert ticket_dict["subject"] == "Refund request"
    assert ticket_dict["status"] == "Closed"
    assert ticket_dict["priority"] == "Low"
    assert isinstance(ticket_dict["created_at"], datetime)
    assert isinstance(ticket_dict["updated_at"], datetime)
    assert ticket_dict["created_at"] == datetime(2025, 1, 1, 9, 0, 0)
    assert ticket_dict["updated_at"] == datetime(2025, 1, 1, 10, 0, 0)
