import pytest
from unittest.mock import MagicMock

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
            "order_id": 1,
            "user_id": 1,
            "address": "123 Street",
            "city": "Indiana",
            "state": "Pennsylvania",
            "postal_code": "15701",
            "country": "United States",
            "delivery_status": "delivered"
        },
        {
            "order_id": 2,
            "user_id": 1,
            "address": "123 Street",
            "city": "Indiana",
            "state": "Pennsylvania",
            "postal_code": "15701",
            "country": "United States",
            "delivery_status": "delivered"
        }
    ]

    deliveries = DeliveryMapper.get_all_deliveries(db_session=mock_db_session)

    assert len(deliveries) == 2
    assert deliveries[0]["user_id"] == 1
    assert deliveries[1]["user_id"] == 1
    assert isinstance(deliveries[0]["address"], str)
    assert isinstance(deliveries[1]["address"], str)


def test_get_delivery_by_id(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.return_value = {
        "order_id": 1,
        "user_id": 1,
        "address": "123 Street",
        "city": "Indiana",
        "state": "Pennsylvania",
        "postal_code": "15701",
        "country": "United States",
        "delivery_status": "delivered"
    }

    delivery = DeliveryMapper.get_delivery_by_id(delivery_id=1, db_session=mock_db_session)

    assert delivery["order_id"] == 1
    assert delivery["user_id"] == 1
    assert isinstance(delivery["address"], str)


def test_create_delivery(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
        "order_id": 1,
        "user_id": 1,
        "address": "123 Street",
        "city": "Indiana",
        "state": "Pennsylvania",
        "postal_code": "15701",
        "country": "United States",
        "delivery_status": "delivered"
    }

    delivery_id = DeliveryMapper.create_delivery(data=data, db_session=mock_db_session)

    assert delivery_id == 3


def test_delete_delivery(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1

    rows_deleted = DeliveryMapper.delete_delivery(delivery_id=1, db_session=mock_db_session)

    assert rows_deleted == 1


def test_create_delivery_missing_fields(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
        "order_id": 1,
        "user_id": 1,
        "address": "123 Street",
        "city": "Indiana",
        "state": "Pennsylvania",
        "postal_code": "15701",
        "country": "United States",
        "delivery_status": "delivered"
    }

    del data["user_id"]

    with pytest.raises(expected_exception=TypeError):
        DeliveryMapper.create_delivery(data=data, db_session=mock_db_session)


# noinspection PyDictCreation
def test_create_delivery_invalid_data_type(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
        "order_id": 1,
        "user_id": 1,
        "address": "123 Street",
        "city": "Indiana",
        "state": "Pennsylvania",
        "postal_code": "15701",
        "country": "United States",
        "delivery_status": "delivered"
    }

    data["address"] = 1

    with pytest.raises(expected_exception=TypeError):
        DeliveryMapper.create_delivery(data=data, db_session=mock_db_session)


def test_get_delivery_by_id_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.side_effect = Exception("Database error")

    with pytest.raises(expected_exception=Exception, match="Database error"):
        DeliveryMapper.get_delivery_by_id(delivery_id=1, db_session=mock_db_session)


def test_get_all_deliveries_no_results(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchall.return_value = []

    deliveries = DeliveryMapper.get_all_deliveries(db_session=mock_db_session)

    assert len(deliveries) == 0


def test_create_delivery_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.execute.side_effect = Exception("Database error")

    data = {
        "order_id": 1,
        "user_id": 1,
        "address": "123 Street",
        "city": "Indiana",
        "state": "Pennsylvania",
        "postal_code": "15701",
        "country": "United States",
        "delivery_status": "delivered"
    }

    with pytest.raises(expected_exception=Exception, match="Database error"):
        DeliveryMapper.create_delivery(data=data, db_session=mock_db_session)


def test_delete_delivery_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.execute.side_effect = Exception("Database error")

    with pytest.raises(expected_exception=Exception, match="Database error"):
        DeliveryMapper.delete_delivery(1, db_session=mock_db_session)
