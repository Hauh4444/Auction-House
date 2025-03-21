import pytest
from datetime import datetime
from app.entities import Order

def test_order_creation():
    order = Order(
        user_id=1,
        order_date=datetime(2025, 1, 1),
        status="delivered",
    )

    assert order.user_id == 1
    assert order.order_date == datetime(2025, 1, 1)
    assert order.status == "delivered"
    assert isinstance(order.created_at, datetime)
    assert isinstance(order.updated_at, datetime)

def test_order_with_optional_fields():
    order = Order(
        order_id=1,
        user_id=1,
        order_date=datetime(2025, 1, 1),
        status="delivered",
        created_at=datetime(2025, 1, 1),
        updated_at=datetime(2025, 1, 1),
    )

    assert order.order_id == 1
    assert order.created_at == datetime(2025, 1, 1)
    assert order.updated_at == datetime(2025, 1, 1)
    assert isinstance(order.created_at, datetime)
    assert isinstance(order.updated_at, datetime)

def test_order_to_dict():
    order = Order(
        order_id=1,
        user_id=1,
        order_date=datetime(2025, 1, 1),
        status="delivered",
        created_at=datetime(2025, 1, 1),
        updated_at=datetime(2025, 1, 1),
    )

    order_dict = order.to_dict()

    assert order_dict["order_id"] == 1
    assert order_dict["user_id"] == 1
    assert order_dict["order_date"] == datetime(2025, 1, 1)
    assert order_dict["status"] == "delivered"
    assert order_dict["created_at"] == datetime(2025, 1, 1)
    assert order_dict["updated_at"] == datetime(2025, 1, 1)

def test_order_missing_required_fields():
    with pytest.raises(TypeError):
        Order()

def test_order_invalid_types():
    with pytest.raises(TypeError):
        Order(
            order_id=1,
            user_id="invalid_type",
            order_date=datetime(2025, 1, 1),
            status="delivered",
            created_at=datetime(2025, 1, 1),
            updated_at=datetime(2025, 1, 1),
        )
    
    with pytest.raises(ValueError):
        Order(
            order_id=1,
            user_id=1,
            order_date=datetime(2025, 1, 1),
            status="invalid_value",
            created_at=datetime(2025, 1, 1),
            updated_at=datetime(2025, 1, 1),
        )
