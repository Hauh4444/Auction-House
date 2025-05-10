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
            "order_id": 1,
            "user_id": 1,
            "order_date": datetime(2025, 1, 1),
            "status": "delivered",
            "created_at": datetime(2025, 1, 1),
            "updated_at": datetime(2025, 1, 1),
        },
        {
            "order_id": 2,
            "user_id": 1,
            "order_date": datetime(2025, 1, 1),
            "status": "shipped",
            "created_at": datetime(2025, 1, 1),
            "updated_at": datetime(2025, 1, 1),
        }
    ]
    orders = OrderMapper.get_all_orders(user_id=1, db_session=mock_db_session)

    assert len(orders) == 2
    assert orders[0]["status"] == "delivered"
    assert orders[1]["status"] == "shipped"
    assert isinstance(orders[0]["created_at"], datetime)
    assert isinstance(orders[1]["created_at"], datetime)


def test_get_order_by_id(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.return_value = {
        "order_id": 2,
        "user_id": 1,
        "order_date": datetime(2025, 1, 1),
        "status": "delivered",
        "created_at": datetime(2025, 1, 1),
        "updated_at": datetime(2025, 1, 1),
    }

    order = OrderMapper.get_order_by_id(order_id=2, db_session=mock_db_session)

    assert order["order_id"] == 2
    assert order["status"] == "delivered"
    assert isinstance(order["created_at"], datetime)


def test_create_order(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
        "user_id": 1,
        "order_date": datetime(2025, 1, 1),
        "status": "delivered",
    }

    created_order = OrderMapper.create_order(data=data, db_session=mock_db_session)

    assert created_order == 3


def test_update_order(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1
    data = {
        "order_date": datetime(2025, 1, 1),
        "status": "delivered",
    }

    rows_updated = OrderMapper.update_order(order_id=3, data=data, db_session=mock_db_session)

    assert rows_updated == 1


def test_delete_order(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1

    rows_deleted = OrderMapper.delete_order(order_id=1, db_session=mock_db_session)

    assert rows_deleted == 1
