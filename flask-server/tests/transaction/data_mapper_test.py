import pytest
from unittest.mock import MagicMock
from datetime import datetime

from app.data_mappers import TransactionMapper

@pytest.fixture
def mock_db_session():
    session = MagicMock()
    session.cursor.return_value = session
    return session

def test_get_all_transactions(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchall.return_value = [
        {
            "transaction_id": 1,
            "order_id": 10,
            "user_id": 1,
            "transaction_date": datetime(2024, 1, 1),
            "transaction_type": "auction",
            "amount": 150.00,
            "shipping_cost": 10.00,
            "payment_method": "VISA",
            "payment_status": "completed",
            "created_at": datetime(2024, 1, 1),
            "updated_at": datetime(2024, 1, 3)
        },
        {
            "transaction_id": 2,
            "order_id": 12,
            "user_id": 1,
            "transaction_date": datetime(2024, 2, 1),
            "transaction_type": "buy_now",
            "amount": 200.00,
            "shipping_cost": 15.00,
            "payment_method": "PAYPAL",
            "payment_status": "pending",
            "created_at": datetime(2024, 2, 1),
            "updated_at": datetime(2024, 2, 3)
        }
    ]

    transactions = TransactionMapper.get_all_transactions(user_id=1, db_session=mock_db_session)
    
    assert len(transactions) == 2
    assert transactions[0]["amount"] == 150.00
    assert transactions[1]["payment_method"] == "PAYPAL"
    assert isinstance(transactions[0]["created_at"], datetime)

def test_get_transaction_by_id(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.return_value = {
        "transaction_id": 1,
        "order_id": 10,
        "user_id": 1,
        "transaction_date": datetime(2024, 1, 1),
        "transaction_type": "buy_now",
        "amount": 150.00,
        "shipping_cost": 12.00,
        "payment_method": "VISA",
        "payment_status": "completed",
        "created_at": datetime(2024, 1, 1),
        "updated_at": datetime(2024, 1, 3)
    }

    transaction = TransactionMapper.get_transaction_by_id(transaction_id=1, db_session=mock_db_session)

    assert transaction["transaction_id"] == 1
    assert transaction["payment_status"] == "completed"

def test_create_transaction(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
        "order_id": 20,
        "user_id": 5,
        "transaction_date": datetime(2025, 3, 3),
        "transaction_type": "auction",
        "amount": 250.00,
        "shipping_cost": 20.00,
        "payment_method": "MASTERCARD",
        "payment_status": "completed",
        "created_at": datetime(2025, 3, 3),
        "updated_at": datetime(2025, 3, 5)
    }

    created_transaction = TransactionMapper.create_transaction(data=data, db_session=mock_db_session)

    assert created_transaction == 3

def test_update_transaction(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1
    data = {
        "payment_status": "refunded",
        "amount": 100.00
    }

    rows_updated = TransactionMapper.update_transaction(transaction_id=1, data=data, db_session=mock_db_session)

    assert rows_updated == 1

def test_delete_transaction(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1

    rows_deleted = TransactionMapper.delete_transaction(transaction_id=1, db_session=mock_db_session)

    assert rows_deleted == 1
