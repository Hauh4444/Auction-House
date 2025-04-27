import pytest
from datetime import datetime
from app.entities import Order


@pytest.fixture
def mock_db_session():
    session = MagicMock()
    return session


def test_order_creation():
    order = Order(
        user_id=1,
        order_date=datetime(2025, 4, 27, 14, 30, 0),
        status="pending"
    )

    assert order.user_id == 1
    assert order.order_date == datetime(2025, 4, 27, 14, 30, 0)
    assert order.status == "pending"
    assert isinstance(order.order_id, (int, type(None)))  # Optional field
    assert isinstance(order.user_id, int)
    assert isinstance(order.order_date, datetime)
    assert isinstance(order.status, str)
    assert isinstance(order.created_at, str)
    assert isinstance(order.updated_at, str)


def test_order_with_optional_fields():
    order = Order(
        order_id=123,
        user_id=1,
        order_date=datetime(2025, 4, 27, 14, 30, 0),
        status="shipped",
        created_at=datetime(2025, 4, 25, 10, 0, 0),
        updated_at=datetime(2025, 4, 26, 12, 0, 0)
    )

    assert order.order_id == 123
    assert order.user_id == 1
    assert order.status == "shipped"
    assert order.created_at == datetime(2025, 4, 25, 10, 0, 0)
    assert order.updated_at == datetime(2025, 4, 26, 12, 0, 0)
    assert isinstance(order.order_id, int)
    assert isinstance(order.user_id, int)
    assert isinstance(order.order_date, datetime)
    assert isinstance(order.status, str)
    assert isinstance(order.created_at, datetime)
    assert isinstance(order.updated_at, datetime)


def test_order_invalid_status():
    with pytest.raises(ValueError):
        Order(
            user_id=1,
            order_date=datetime(2025, 4, 27, 14, 30, 0),
            status="invalid_status"
        )


def test_order_to_dict():
    order = Order(
        order_id=123,
        user_id=1,
        order_date=datetime(2025, 4, 27, 14, 30, 0),
        status="shipped",
        created_at=datetime(2025, 4, 25, 10, 0, 0),
        updated_at=datetime(2025, 4, 26, 12, 0, 0)
    )

    order_dict = order.to_dict()

    assert order_dict["order_id"] == 123
    assert order_dict["user_id"] == 1
    assert order_dict["order_date"] == "2025-04-27 14:30:00"
    assert order_dict["status"] == "shipped"
    assert order_dict["created_at"] == "2025-04-25 10:00:00"
    assert order_dict["updated_at"] == "2025-04-26 12:00:00"
    assert isinstance(order_dict["order_id"], int)
    assert isinstance(order_dict["user_id"], int)
    assert isinstance(order_dict["order_date"], str)
    assert isinstance(order_dict["status"], str)
    assert isinstance(order_dict["created_at"], str)
    assert isinstance(order_dict["updated_at"], str)


def test_order_missing_required_fields():
    with pytest.raises(TypeError):
        Order()


def test_order_invalid_types():
    with pytest.raises(TypeError):
        Order(
            order_id="123",  # Invalid type for order_id
            user_id="1",  # Invalid type for user_id
            order_date="2025-04-27 14:30:00",  # Invalid type for order_date
            created_at="2025-04-25 10:00:00",  # Invalid type for created_at
            updated_at="2025-04-26 12:00:00"  # Invalid type for updated_at
        )
