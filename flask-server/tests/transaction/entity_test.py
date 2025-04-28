import pytest
from datetime import datetime
from app.entities import Transaction

def test_transaction_creation():
    transaction = Transaction(
        order_id=1,
        user_id=2,
        transaction_date=datetime(2024, 3, 18, 12, 0, 0),
        transaction_type="buy_now",
        amount=150.75,
        shipping_cost=10.00,
        payment_method="Credit Card",
        payment_status="pending"
    )
    
    assert transaction.order_id == 1
    assert transaction.user_id == 2
    assert transaction.transaction_date == datetime(2024, 3, 18, 12, 0, 0)
    assert transaction.transaction_type == "buy_now"
    assert transaction.amount == 150.75
    assert transaction.shipping_cost == 10.00
    assert transaction.payment_method == "Credit Card"
    assert transaction.payment_status == "pending"
    assert isinstance(transaction.created_at, datetime)  # It's saved as a string (due to strftime)
    assert isinstance(transaction.updated_at, datetime)

def test_transaction_with_optional_fields():
    transaction = Transaction(
        transaction_id=10,
        order_id=4,
        user_id=5,
        transaction_date=datetime(2024, 3, 19, 14, 30, 0),
        transaction_type="auction",
        amount=250.00,
        shipping_cost=20.00,
        payment_method="PayPal",
        payment_status="completed",
        created_at=datetime(2024, 3, 18, 10, 0, 0),
        updated_at=datetime(2024, 3, 18, 12, 0, 0)
    )
    
    assert transaction.transaction_id == 10
    assert transaction.created_at == datetime(2024, 3, 18, 10, 0, 0)
    assert transaction.updated_at == datetime(2024, 3, 18, 12, 0, 0)

def test_transaction_to_dict():
    transaction = Transaction(
        transaction_id=7,
        order_id=8,
        user_id=9,
        transaction_date=datetime(2024, 3, 20, 16, 45, 0),
        transaction_type="buy_now",
        amount=75.00,
        shipping_cost=5.00,
        payment_method="Bank Transfer",
        payment_status="completed"
    )
    
    transaction_dict = transaction.to_dict()
    
    assert transaction_dict["transaction_id"] == 7
    assert transaction_dict["order_id"] == 8
    assert transaction_dict["user_id"] == 9
    assert transaction_dict["transaction_date"] == "2024-03-20 16:45:00"
    assert transaction_dict["transaction_type"] == "buy_now"
    assert transaction_dict["amount"] == 75.00
    assert transaction_dict["shipping_cost"] == 5.00
    assert transaction_dict["payment_method"] == "Bank Transfer"
    assert transaction_dict["payment_status"] == "completed"

def test_transaction_missing_required_fields():
    with pytest.raises(TypeError):
        Transaction()

def test_transaction_invalid_values():
    # Invalid transaction_type
    with pytest.raises(ValueError):
        Transaction(
            order_id=1,
            user_id=2,
            transaction_date=datetime(2024, 3, 18, 12, 0, 0),
            transaction_type="invalid_type",
            amount=50.00,
            shipping_cost=5.00,
            payment_method="Credit Card",
            payment_status="completed"
        )

    # Invalid payment_status
    with pytest.raises(ValueError):
        Transaction(
            order_id=1,
            user_id=2,
            transaction_date=datetime(2024, 3, 18, 12, 0, 0),
            transaction_type="buy_now",
            amount=50.00,
            shipping_cost=5.00,
            payment_method="Credit Card",
            payment_status="invalid_status"
        )
