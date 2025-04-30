import pytest
from unittest.mock import MagicMock
from datetime import datetime

from app.data_mappers import DeliveryMapper

@pytest.fixture
def mock_db_session():
    session = MagicMock()
    session.cursor.return_value = session
    return session


def test_get_all_deliveries(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchall.return_value = [
        {
            "delivery_id": 1,
            "order_item_id": 101,
            "user_id": 1,
            "address": "123 Main St",
            "city": "Cityville",
            "state": "CA",
            "country": "USA",
            "delivery_status": "shipped",
            "tracking_number": "ABC123",
            "courier": "CourierX",
            "estimated_delivery_date": datetime(2023, 5, 10),
            "delivered_at": None,
            "created_at": datetime(2023, 1, 1, 12, 0, 0),
            "updated_at": datetime(2023, 1, 2, 12, 0, 0)
        },
        {
            "delivery_id": 2,
            "order_item_id": 102,
            "user_id": 2,
            "address": "456 Elm St",
            "city": "Townsville",
            "state": "TX",
            "country": "USA",
            "delivery_status": "delivered",
            "tracking_number": "DEF456",
            "courier": "CourierY",
            "estimated_delivery_date": datetime(2023, 5, 11),
            "delivered_at": datetime(2023, 5, 10),
            "created_at": datetime(2023, 2, 1, 12, 0, 0),
            "updated_at": datetime(2023, 2, 2, 12, 0, 0)
        }
    ]

    deliveries = DeliveryMapper.get_all_deliveries(user_id=1, db_session=mock_db_session)

    assert len(deliveries) == 2
    assert deliveries[0]["address"] == "123 Main St"
    assert deliveries[1]["address"] == "456 Elm St"
    # Check if created_at is a string (formatted properly)
    assert isinstance(deliveries[0]["created_at"], datetime)
    assert isinstance(deliveries[1]["created_at"], datetime)


def test_get_delivery_by_id(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.return_value = {
        "delivery_id": 1,
        "order_item_id": 101,
        "user_id": 1,
        "address": "123 Main St",
        "city": "Cityville",
        "state": "CA",
        "country": "USA",
        "delivery_status": "processing",
        "tracking_number": "ABC123",
        "courier": "CourierX",
        "estimated_delivery_date": datetime(2023, 5, 10),
        "delivered_at": None,
        "created_at": datetime(2023, 1, 1, 12, 0, 0),
        "updated_at": datetime(2023, 1, 2, 12, 0, 0)
    }

    delivery = DeliveryMapper.get_delivery_by_id(delivery_id=1, db_session=mock_db_session)

    assert delivery["delivery_id"] == 1
    assert delivery["address"] == "123 Main St"
    # Check if created_at is a string
    assert isinstance(delivery["created_at"], datetime)
    assert isinstance(delivery["updated_at"], datetime)


def test_create_delivery(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
        "order_item_id": 103,
        "user_id": 1,
        "address": "789 Oak St",
        "city": "Villageville",
        "state": "FL",
        "country": "USA",
        "delivery_status": "delivered",
        "tracking_number": "GHI789",
        "courier": "CourierZ",
        "estimated_delivery_date": datetime(2023, 5, 12),
        "delivered_at": None,
        "created_at": datetime(2023, 3, 1, 12, 0, 0),
        "updated_at": datetime(2023, 3, 2, 12, 0, 0)
    }

    delivery_id = DeliveryMapper.create_delivery(data=data, db_session=mock_db_session)

    assert delivery_id == 3


def test_update_delivery(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1
    data = {
        "delivery_status": "Delivered",
        "delivered_at": datetime(2023, 5, 10),
        "updated_at": datetime(2023, 4, 1, 12, 0, 0)
    }

    rows_updated = DeliveryMapper.update_delivery(delivery_id=1, data=data, db_session=mock_db_session)

    assert rows_updated == 1


def test_delete_delivery(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1

    rows_deleted = DeliveryMapper.delete_delivery(delivery_id=1, db_session=mock_db_session)

    assert rows_deleted == 1
