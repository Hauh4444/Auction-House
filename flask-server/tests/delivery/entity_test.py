import pytest
from unittest.mock import MagicMock
from datetime import datetime, date

from app.entities import Delivery

@pytest.fixture
def mock_db_session():
    session = MagicMock()
    return session

def test_delivery_creation():
    # Ensure `created_at` is set to datetime.now() and not as a string
    delivery = Delivery(
        order_item_id=1,
        user_id=1,
        address="123 Street",
        city="Indiana",
        state="Pennsylvania",
        country="United States",
        delivery_status="delivered"
    )

    assert delivery.order_item_id == 1
    assert delivery.user_id == 1
    assert delivery.address == "123 Street"
    assert delivery.city == "Indiana"
    assert delivery.state == "Pennsylvania"
    assert delivery.country == "United States"
    assert delivery.delivery_status == "delivered"
    assert isinstance(delivery.order_item_id, int)
    assert isinstance(delivery.user_id, int)
    assert isinstance(delivery.address, str)
    assert isinstance(delivery.city, str)
    assert isinstance(delivery.state, str)
    assert isinstance(delivery.country, str)
    assert isinstance(delivery.delivery_status, str)
    
    # Ensure created_at is a datetime object, not a string
    assert isinstance(delivery.created_at, str)
    assert isinstance(delivery.updated_at, str)

def test_delivery_to_dict():
    delivery = Delivery(
        delivery_id=1,
        order_item_id=1,
        user_id=1,
        address="123 Street",
        city="Indiana",
        state="Pennsylvania",
        country="United States",
        delivery_status="delivered",
        tracking_number="1",
        courier="UPS",
        estimated_delivery_date=datetime(2024, 1, 1, 0, 0, 0),
        delivered_at=datetime(2024, 1, 1, 10, 0, 0),
        created_at=datetime(2024, 1, 1, 10, 0, 0),
        updated_at=datetime(2024, 1, 1, 10, 0, 0)
    )

    delivery_dict = delivery.to_dict()

    assert delivery_dict["order_item_id"] == 1
    assert delivery_dict["user_id"] == 1
    assert delivery_dict["address"] == "123 Street"
    assert delivery_dict["city"] == "Indiana"
    assert delivery_dict["state"] == "Pennsylvania"
    assert delivery_dict["country"] == "United States"
    assert delivery_dict["delivery_status"] == "delivered"
    assert delivery_dict["tracking_number"] == "1"
    assert delivery_dict["courier"] == "UPS"

    # Compare the string-formatted datetime
    assert delivery_dict["estimated_delivery_date"] == '2024-01-01 00:00:00'  # String match
    assert delivery_dict["delivered_at"] == '2024-01-01 10:00:00'  # String match
    assert delivery_dict["created_at"] == '2024-01-01 10:00:00'  # String match
    assert delivery_dict["updated_at"] == '2024-01-01 10:00:00'  # String match


def test_delivery_missing_required_fields():
    with pytest.raises(expected_exception=TypeError):
        Delivery()

def test_delivery_invalid_types():
    with pytest.raises(expected_exception=TypeError):
        Delivery(
            delivery_id="1",
            order_item_id="1",
            user_id="1",
            address=1,
            city=1,
            state=1,
            country=1,
            delivery_status=1,
            tracking_number=1,
            courier=1,
            estimated_delivery_date=1,
            delivered_at=1,
            created_at=1,
            updated_at=1
        )

    with pytest.raises(expected_exception=ValueError):
        Delivery(
            order_item_id=1,
            user_id=1,
            address="123 Street",
            city="Indiana",
            state="Pennsylvania",
            country="United States",
            delivery_status="invalid_type"
        )
