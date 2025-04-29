import pytest
from unittest.mock import MagicMock
from datetime import datetime

from app.data_mappers import SupportTicketMapper


@pytest.fixture
def mock_db_session():
    session = MagicMock()
    session.cursor.return_value = session
    return session


def test_get_ticket_by_id(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.return_value = {
        "ticket_id": 1, "user_id": 10, "subject": "Issue with order",
        "status": "open", "priority": "high", "assigned_to": "SupportAgent",
        "created_at": datetime(2024, 1, 1), "updated_at": datetime(2024, 1, 3)
    }

    ticket = SupportTicketMapper.get_ticket_by_id(ticket_id=1, db_session=mock_db_session)

    assert ticket["ticket_id"] == 1
    assert ticket["status"] == "open"


def test_get_tickets_by_user_id(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchall.return_value = [
        {
            "ticket_id": 1, "user_id": 10, "subject": "Issue with order",
            "status": "open", "priority": "high", "assigned_to": "SupportAgent",
            "created_at": datetime(2024, 1, 1), "updated_at": datetime(2024, 1, 3)
        },
        {
            "ticket_id": 2, "user_id": 10, "subject": "Delayed shipment",
            "status": "pending", "priority": "medium", "assigned_to": "SupportAgent2",
            "created_at": datetime(2024, 2, 1), "updated_at": datetime(2024, 2, 3)
        }
    ]
    
    tickets = SupportTicketMapper.get_tickets_by_user_id(user_id=10, db_session=mock_db_session)
    
    assert len(tickets) == 2
    assert tickets[0]["subject"] == "Issue with order"
    assert tickets[1]["subject"] == "Delayed shipment"


def test_create_ticket(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
        "user_id": 12, "subject": "Payment issue",
        "status": "open", "priority": "low", "assigned_to": "SupportAgent3",
        "created_at": datetime(2025, 3, 3), "updated_at": datetime(2025, 3, 5)
    }

    created_ticket = SupportTicketMapper.create_ticket(data=data, db_session=mock_db_session)

    assert created_ticket == 3


def test_update_ticket(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1
    data = {
        "status": "resolved",
        "priority": "low"
    }

    rows_updated = SupportTicketMapper.update_ticket(ticket_id=1, data=data, db_session=mock_db_session)

    assert rows_updated == 1


def test_delete_ticket(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1

    rows_deleted = SupportTicketMapper.delete_ticket(ticket_id=1, db_session=mock_db_session)

    assert rows_deleted == 1

def test_create_ticket_missing_fields(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
        "user_id": 10, "subject": "New issue", 
        "status": "open", "priority": "medium", "assigned_to": "support_agent", 
        "created_at": datetime(2024, 3, 1), "updated_at": datetime(2024, 3, 1)
    }

    del data["status"]

    with pytest.raises(expected_exception=TypeError):
        SupportTicketMapper.create_ticket(data=data, db_session=mock_db_session)


def test_get_ticket_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.side_effect = Exception("Database error")

    with pytest.raises(expected_exception=Exception, match="Database error"):
        SupportTicketMapper.get_ticket_by_id(ticket_id=1, db_session=mock_db_session)


def test_create_ticket_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.execute.side_effect = Exception("Database error")
    data = {
        "user_id": 10, "subject": "New issue", 
        "status": "open", "priority": "medium", "assigned_to": "support_agent", 
        "created_at": datetime(2024, 3, 1), "updated_at": datetime(2024, 3, 1)
    }

    with pytest.raises(expected_exception=Exception, match="Database error"):
        SupportTicketMapper.create_ticket(data=data, db_session=mock_db_session)


def test_update_ticket_invalid_id(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 0  # Simulate no rows were updated

    data = {
        "status": "closed", "priority": "high", "assigned_to": "senior_support_agent"
    }

    rows_updated = SupportTicketMapper.update_ticket(ticket_id=999, data=data, db_session=mock_db_session)  # Invalid ID

    assert rows_updated == 0  # Expecting no rows to be updated


def test_delete_ticket_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.execute.side_effect = Exception("Database error")

    with pytest.raises(expected_exception=Exception, match="Database error"):
        SupportTicketMapper.delete_ticket(ticket_id=1, db_session=mock_db_session)