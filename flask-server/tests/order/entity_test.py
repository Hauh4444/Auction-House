import pytest
from datetime import datetime
from app.entities import Order

def test_order_creation():
    order = Order(
        user_id=1,
        order_date=datetime(2024, 3, 18, 12, 0, 0),
        status="processing",
        total_amount=100.50,
        payment_status="pending",
        payment_method="Credit Card",
        shipping_address="123 Street, City, Country",
        shipping_method="Standard"
    )

    assert order.user_id == 1
    assert order.status == "processing"
    assert order.total_amount == 100.50
    assert order.payment_status == "pending"
    assert order.payment_method == "Credit Card"
    assert order.shipping_address == "123 Street, City, Country"
    assert order.shipping_method == "Standard"
    assert isinstance(order.created_at, datetime)
    assert isinstance(order.updated_at, datetime)

def test_order_with_optional_fields():
    order = Order(
        order_id=10,
        user_id=2,
        order_date=datetime(2024, 3, 18, 14, 30, 0),
        status="shipped",
        total_amount=250.75,
        payment_status="completed",
        payment_method="PayPal",
        shipping_address="456 Avenue, City, Country",
        shipping_method="Express",
        tracking_number="TRACK123",
        shipping_cost=15.00,
        created_at=datetime(2024, 3, 18, 10, 0, 0),
        updated_at=datetime(2024, 3, 18, 12, 0, 0)
    )

    assert order.order_id == 10
    assert order.tracking_number == "TRACK123"
    assert order.shipping_cost == 15.00
    assert isinstance(order.created_at, datetime)
    assert isinstance(order.updated_at, datetime)

def test_order_to_dict():
    order = Order(
        order_id=5,
        user_id=3,
        order_date=datetime(2024, 3, 18, 16, 45, 0),
        status="delivered",
        total_amount=75.00,
        payment_status="completed",
        payment_method="Bank Transfer",
        shipping_address="789 Boulevard, City, Country",
        shipping_method="Overnight"
    )

    order_dict = order.to_dict()

    assert order_dict["order_id"] == 5
    assert order_dict["status"] == "delivered"
    assert order_dict["total_amount"] == 75.00
    assert order_dict["payment_status"] == "completed"
    assert order_dict["shipping_address"] == "789 Boulevard, City, Country"
    assert order_dict["shipping_method"] == "Overnight"

def test_order_missing_required_fields():
    with pytest.raises(TypeError):
        Order()

def test_order_invalid_types():
    with pytest.raises(TypeError):
        Order(
            order_id="10",
            user_id="user",
            order_date="invalid date",
            status=123,
            listing_type="standard",
            total_amount="100.50",
            payment_status=456,
            payment_method=789,
            shipping_address=101112,
            shipping_method=[]
        )
    
    with pytest.raises(ValueError):
        Order(
            user_id=1,
            order_date=datetime(2024, 3, 18, 12, 0, 0),
            status="invalid_status",
            total_amount=50.00,
            payment_status="invalid_payment_status",
            payment_method="Credit Card",
            shipping_address="123 Street",
            shipping_method="Standard"
        )
