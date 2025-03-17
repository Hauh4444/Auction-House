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
            "transaction_id": 1, "listing_id": 100, "buyer_id": 10, "seller_id": 20,
            "transaction_date": datetime(2024, 1, 1), "transaction_type": "auction", "amount": 150.00,
            "payment_method": "VISA", "status": "completed", "shipping_address": "123 Main St",
            "tracking_number": "94009340434321239384", "created_at": datetime(2024, 1, 1), "updated_at": datetime(2024, 1, 3)
        },
        {
            "transaction_id": 2, "listing_id": 101, "buyer_id": 11, "seller_id": 21,
            "transaction_date": datetime(2024, 2, 1), "transaction_type": "buy_now", "amount": 200.00,
            "payment_method": "PAYPAL", "status": "pending", "shipping_address": "456 Oak St",
            "tracking_number": "9610 1385 2890", "created_at": datetime(2024, 2, 1), "updated_at": datetime(2024, 2, 3)
        }
    ]
    
    transactions = TransactionMapper.get_all_transactions(db_session=mock_db_session)
    
    assert len(transactions) == 2
    assert transactions[0]["amount"] == 150.00
    assert transactions[1]["payment_method"] == "PAYPAL"
    assert isinstance(transactions[0]["created_at"], datetime)


def test_get_transaction_by_id(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.return_value = {
        "transaction_id": 1, "listing_id": 100, "buyer_id": 10, "seller_id": 20,
        "transaction_date": datetime(2024, 1, 1), "transaction_type": "buy_now", "amount": 150.00,
        "payment_method": "VISA", "status": "completed", "shipping_address": "123 Main St",
        "tracking_number": "94009340434321239384", "created_at": datetime(2024, 1, 1), "updated_at": datetime(2024, 1, 3)
    }

    transaction = TransactionMapper.get_transaction_by_id(transaction_id=1, db_session=mock_db_session)

    assert transaction["transaction_id"] == 1
    assert transaction["status"] == "completed"


def test_create_transaction(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
        "listing_id": 102, "buyer_id": 12, "seller_id": 22,
        "transaction_date": datetime(2025, 3, 3), "transaction_type": "auction", "amount": 250.00,
        "payment_method": "MASTERCARD", "status": "completed", "shipping_address": "789 Pine St",
        "tracking_number": "1234567890", "created_at": datetime(2025, 3, 3), "updated_at": datetime(2025, 3, 5)
    }

    created_transaction = TransactionMapper.create_transaction(data=data, db_session=mock_db_session)

    assert created_transaction == 3


def test_update_transaction(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1
    data = {
        "status": "refunded",
        "amount": 100.00
    }

    rows_updated = TransactionMapper.update_transaction(transaction_id=1, data=data, db_session=mock_db_session)

    assert rows_updated == 1


def test_delete_transaction(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1

    rows_deleted = TransactionMapper.delete_transaction(transaction_id=1, db_session=mock_db_session)

    assert rows_deleted == 1
