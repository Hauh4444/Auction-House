import pytest
from unittest.mock import MagicMock
from datetime import datetime

from app.data_mappers import OrderMapper


@pytest.fixture
def mock_db_session():
    session = MagicMock()
    session.cursor.return_value = session
    return session


def test_get_all_orders(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchall.return_value = [
        {
            "order_id": 1, "user_id": 1, "order_date": datetime(2024, 1, 1), "status": "shipped",
            "total_amount": 25.99, "payment_status": "pending", "payment_method": "VISA", "shipping_address": "123 Main St Indiana PA 15701",
            "shipping_method": "USPS", "tracking_number": "94009340434321239384", "shipping_cost": 5.39, "created_at": datetime(2024, 1, 1),
            "updated_at": datetime(2024, 1, 3)
        },
        {
            "order_id": 2, "user_id": 1, "order_date": datetime(2025, 1, 1), "status": "shipped",
            "total_amount": 205.99, "payment_status": "completed", "payment_method": "MASTERCARD", "shipping_address": "69 Nice St Intercourse PA 17534",
            "shipping_method": "FEDEX", "tracking_number": "9610 1385 2890", "shipping_cost": 15.39, "created_at": datetime(2025, 1, 1),
            "updated_at": datetime(2025, 1, 3)  
        }
    ]
    orders = OrderMapper.get_all_orders(db_session=mock_db_session)

    assert len(orders) == 2
    assert orders[0]["shipping_address"] == "123 Main St Indiana PA 15701"
    assert orders[1]["shipping_address"] == "69 Nice St Intercourse PA 17534"
    assert isinstance(orders[0]["created_at"], datetime)
    assert isinstance(orders[1]["created_at"], datetime)

def test_get_order_by_id(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.return_value = {
            "order_id": 2, "user_id": 1, "order_date": datetime(2025, 1, 1), "status": "shipped",
            "total_amount": 205.99, "payment_status": "pending", "payment_method": "MASTERCARD", "shipping_address": "69 Nice St Intercourse PA 17534",
            "shipping_method": "FEDEX", "tracking_number": "9610 1385 2890", "shipping_cost": 15.39, "created_at": datetime(2025, 1, 1),
            "updated_at": datetime(2025, 1, 3) 
    }

    order_num = OrderMapper.get_order_by_id(order_id=2, db_session=mock_db_session)

    assert order_num["order_id"] == 2
    assert order_num["shipping_method"] == "FEDEX"

def test_create_order(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
            "order_id": 4, "user_id": 1, "order_date": datetime(2025, 1, 1), "status": "shipped",
            "total_amount": 205.99, "payment_status": "completed", "payment_method": "MASTERCARD", "shipping_address": "69 Nice St Intercourse PA 17534",
            "shipping_method": "FEDEX", "tracking_number": "9610 1385 2890", "shipping_cost": 15.39, "created_at": datetime(2025, 1, 1),
            "updated_at": datetime(2025, 1, 3) 
    }

    created_order = OrderMapper.create_order(data = data, db_session=mock_db_session)

    assert created_order == 3

def test_update_order(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1
    data = {
        "shipping_method": "UPS",
        "tracking_number": "1300ZASADFASDF"
    }

    rows_updated = OrderMapper.update_order(order_id=3, data=data, db_session=mock_db_session)

    assert rows_updated == 1

def test_delete_order(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1

    rows_deleted = OrderMapper.delete_order(order_id=1, db_session=mock_db_session)

    assert rows_deleted == 1


def test_create_order_missing_fields(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
        "user_id": 10, "order_date": datetime(2024, 1, 1), "status": "shipped", "total_amount": 150.0,
        "payment_status": "paid", "payment_method": "credit_card", "shipping_address": "123 Street",
        "shipping_method": "ground", "tracking_number": "XYZ123", "shipping_cost": 5.0, 
        "created_at": datetime(2024, 1, 1), "updated_at": datetime(2024, 1, 2)
    }

    del data["total_amount"]

    with pytest.raises(expected_exception=TypeError):
        OrderMapper.create_order(data=data, db_session=mock_db_session)


def test_get_order_by_id_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.side_effect = Exception("Database error")

    with pytest.raises(expected_exception=Exception, match="Database error"):
        OrderMapper.get_order_by_id(order_id=1, db_session=mock_db_session)


def test_create_order_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.execute.side_effect = Exception("Database error")
    data = {
        "user_id": 10, "order_date": datetime(2024, 1, 1), "status": "shipped", "total_amount": 150.0,
        "payment_status": "pending", "payment_method": "credit_card", "shipping_address": "123 Street",
        "shipping_method": "ground", "tracking_number": "XYZ123", "shipping_cost": 5.0, 
        "created_at": datetime(2024, 1, 1), "updated_at": datetime(2024, 1, 2)
    }

    with pytest.raises(expected_exception=Exception, match="Database error"):
        OrderMapper.create_order(data=data, db_session=mock_db_session)


def test_update_order_invalid_id(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 0  # Simulate no rows were updated

    data = {
        "status": "delivered",
        "shipping_address": "789 Boulevard"
    }

    rows_updated = OrderMapper.update_order(order_id=999, data=data, db_session=mock_db_session)  # Invalid ID

    assert rows_updated == 0  # Expecting no rows to be updated


def test_delete_order_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.execute.side_effect = Exception("Database error")

    with pytest.raises(expected_exception=Exception, match="Database error"):
        OrderMapper.delete_order(order_id=1, db_session=mock_db_session)