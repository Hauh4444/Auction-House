import pytest
from unittest.mock import MagicMock
from datetime import datetime

from app.entities import Order


@pytest.fixture
def mock_db_session():
    session = MagicMock()
    return session


def test_listing_creation():
    order = Order(
        user_id=1,
        order_date=datetime(2024, 1, 1),
        status="pending",
        total_amount=105.99,
        payment_status="completed", # "pending", "completed", "failed", "refunded"
        payment_method="VISA",
        shipping_address="123 Main St Indiana PA 15701",
        shipping_method="UPS",
        tracking_number="ZZZZZZZZZZ",
        shipping_cost=15.99,
        created_at=datetime(2024, 1, 1),
        updated_at=datetime(2024, 1, 5),
        order_id=1
    )

    assert order.user_id == 1
    assert order.order_date == datetime(2024, 1, 1)
    assert order.status == "pending"
    assert order.total_amount == 105.99
    assert order.payment_status == "completed"
    assert order.payment_method == "VISA"
    assert order.shipping_address == "123 Main St Indiana PA 15701"
    assert order.shipping_method == "UPS"
    assert order.tracking_number == "ZZZZZZZZZZ"
    assert order.shipping_cost == 15.99
    assert order.created_at == datetime(2024, 1, 1)
    assert order.updated_at == datetime(2024, 1, 5)
    assert order.order_id == 1
    assert isinstance(order.user_id, int)
    assert isinstance(order.order_date, datetime)
    assert isinstance(order.status, str)
    assert isinstance(order.total_amount, float)
    assert isinstance(order.payment_status, str)
    assert isinstance(order.payment_method, str)
    assert isinstance(order.shipping_address, str)
    assert isinstance(order.shipping_method, str)
    assert isinstance(order.tracking_number, str)
    assert isinstance(order.shipping_cost, float)
    assert isinstance(order.created_at, datetime)
    assert isinstance(order.updated_at, datetime)
