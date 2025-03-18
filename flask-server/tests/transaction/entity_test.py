import pytest
from datetime import datetime
from app.entities import Transaction

def test_transaction_creation():
    transaction = Transaction(
        listing_id=1,
        buyer_id=2,
        seller_id=3,
        transaction_date=datetime(2024, 3, 18, 12, 0, 0),
        transaction_type="buy_now",
        amount=150.75,
        payment_method="Credit Card",
        status="pending",
        shipping_address="123 Street, City, Country"
    )
    
    assert transaction.listing_id == 1
    assert transaction.buyer_id == 2
    assert transaction.seller_id == 3
    assert transaction.transaction_date == datetime(2024, 3, 18, 12, 0, 0)
    assert transaction.transaction_type == "buy_now"
    assert transaction.amount == 150.75
    assert transaction.payment_method == "Credit Card"
    assert transaction.status == "pending"
    assert transaction.shipping_address == "123 Street, City, Country"
    assert isinstance(transaction.created_at, datetime)
    assert isinstance(transaction.updated_at, datetime)

def test_transaction_with_optional_fields():
    transaction = Transaction(
        transaction_id=10,
        listing_id=4,
        buyer_id=5,
        seller_id=6,
        transaction_date=datetime(2024, 3, 19, 14, 30, 0),
        transaction_type="auction",
        amount=250.00,
        payment_method="PayPal",
        status="completed",
        shipping_address="456 Avenue, City, Country",
        tracking_number="TRACK123",
        created_at=datetime(2024, 3, 18, 10, 0, 0),
        updated_at=datetime(2024, 3, 18, 12, 0, 0)
    )
    
    assert transaction.transaction_id == 10
    assert transaction.tracking_number == "TRACK123"
    assert transaction.created_at == datetime(2024, 3, 18, 10, 0, 0)
    assert transaction.updated_at == datetime(2024, 3, 18, 12, 0, 0)

def test_transaction_to_dict():
    transaction = Transaction(
        transaction_id=7,
        listing_id=8,
        buyer_id=9,
        seller_id=10,
        transaction_date=datetime(2024, 3, 20, 16, 45, 0),
        transaction_type="buy_now",
        amount=75.00,
        payment_method="Bank Transfer",
        status="completed",
        shipping_address="789 Boulevard, City, Country"
    )
    
    transaction_dict = transaction.to_dict()
    
    assert transaction_dict["transaction_id"] == 7
    assert transaction_dict["listing_id"] == 8
    assert transaction_dict["buyer_id"] == 9
    assert transaction_dict["seller_id"] == 10
    assert transaction_dict["transaction_date"] == datetime(2024, 3, 20, 16, 45, 0)
    assert transaction_dict["transaction_type"] == "buy_now"
    assert transaction_dict["amount"] == 75.00
    assert transaction_dict["payment_method"] == "Bank Transfer"
    assert transaction_dict["status"] == "completed"
    assert transaction_dict["shipping_address"] == "789 Boulevard, City, Country"

def test_transaction_missing_required_fields():
    with pytest.raises(expected_exception=TypeError):
        Transaction()
"""
def test_transaction_invalid_types():
    with pytest.raises(expected_exception=TypeError):
        Transaction(
            transaction_id="10",
            listing_id="listing",
            buyer_id="buyer",
            seller_id="seller",
            transaction_date="invalid_date",
            transaction_type=123,
            amount="100.50",
            payment_method=456,
            status=789,
            shipping_address=101112
        )
    
    with pytest.raises(expected_exception=ValueError):
        Transaction(
            listing_id=1,
            buyer_id=2,
            seller_id=3,
            transaction_date=datetime(2024, 3, 18, 12, 0, 0),
            transaction_type="invalid_type",
            amount=50.00,
            payment_method="Credit Card",
            status="invalid_status",
            shipping_address="123 Street"
        )
"""