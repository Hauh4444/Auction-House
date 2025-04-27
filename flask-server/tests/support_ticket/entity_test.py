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
    assert isinstance(ticket.created_at, str)  # Now it should be a string
    assert isinstance(ticket.updated_at, str)  # Now it should be a string
    assert len(ticket.created_at) == 19  # Checking for the correct date format length (YYYY-MM-DD HH:MM:SS)
    assert len(ticket.updated_at) == 19  # Checking for the correct date format length (YYYY-MM-DD HH:MM:SS)

def test_support_ticket_with_optional_fields():
    ticket = SupportTicket(
        ticket_id=10,
        user_id=2,
        subject="Damaged item",
        status="In Progress",
        priority="Medium",
        assigned_to=5,
        created_at="2024-03-18 10:00:00",  # Keep as string
        updated_at="2024-03-18 12:00:00"   # Keep as string
    )
    
    assert ticket.ticket_id == 10
    assert ticket.assigned_to == 5
    assert ticket.created_at == "2024-03-18 10:00:00"
    assert ticket.updated_at == "2024-03-18 12:00:00"

def test_support_ticket_to_dict():
    ticket = SupportTicket(
        ticket_id=7,
        user_id=3,
        subject="Refund request",
        status="Closed",
        priority="Low"
    )
    
    ticket_dict = ticket.to_dict()
    
    assert ticket_dict["ticket_id"] == 7
    assert ticket_dict["user_id"] == 3
    assert ticket_dict["subject"] == "Refund request"
    assert ticket_dict["status"] == "Closed"
    assert ticket_dict["priority"] == "Low"
    assert isinstance(ticket_dict["created_at"], str)  # Should be string
    assert isinstance(ticket_dict["updated_at"], str)  # Should be string
    assert len(ticket_dict["created_at"]) == 19  # Checking the correct date format length (YYYY-MM-DD HH:MM:SS)
    assert len(ticket_dict["updated_at"]) == 19  # Checking the correct date format length (YYYY-MM-DD HH:MM:SS)

