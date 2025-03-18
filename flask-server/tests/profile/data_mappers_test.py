import pytest
from unittest.mock import MagicMock
from datetime import datetime

from app.data_mappers import ProfileMapper


@pytest.fixture
def mock_db_session():
    session = MagicMock()
    session.cursor.return_value = session
    return session


def test_get_all_profiles(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchall.return_value = [
        {
            "user_id": 1, "first_name": "John", "last_name": "Doe", "date_of_birth": "1990-01-01",
            "phone_number": "123-456-7890", "address": "123 Main St", "city": "New York", "state": "NY",
            "country": "USA", "profile_picture": "profile1.jpg", "bio": "Hello!", "social_links": "@johndoe",
            "created_at": datetime(2024, 1, 1), "updated_at": datetime(2024, 1, 3)
        },
        {
            "user_id": 2, "first_name": "Jane", "last_name": "Doe", "date_of_birth": "1992-02-02",
            "phone_number": "987-654-3210", "address": "456 Elm St", "city": "Los Angeles", "state": "CA",
            "country": "USA", "profile_picture": "profile2.jpg", "bio": "Hi there!", "social_links": "@janedoe",
            "created_at": datetime(2024, 2, 2), "updated_at": datetime(2024, 2, 5)
        }
    ]
    profiles = ProfileMapper.get_all_profiles(db_session=mock_db_session)

    assert len(profiles) == 2
    assert profiles[0]["first_name"] == "John"
    assert profiles[1]["first_name"] == "Jane"
    assert isinstance(profiles[0]["created_at"], datetime)


def test_get_profile(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.return_value = {
        "user_id": 1, "first_name": "John", "last_name": "Doe", "date_of_birth": "1990-01-01",
        "phone_number": "123-456-7890", "address": "123 Main St", "city": "New York", "state": "NY",
        "country": "USA", "profile_picture": "profile1.jpg", "bio": "Hello!", "social_links": "@johndoe",
        "created_at": datetime(2024, 1, 1), "updated_at": datetime(2024, 1, 3)
    }

    profile = ProfileMapper.get_profile(user_id=1, db_session=mock_db_session)

    assert profile["user_id"] == 1
    assert profile["first_name"] == "John"


def test_create_profile(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
        "user_id": 3, "first_name": "Alice", "last_name": "Smith", "date_of_birth": "1995-03-03",
        "phone_number": "555-123-4567", "address": "789 Maple St", "city": "Chicago", "state": "IL",
        "country": "USA", "profile_picture": "profile3.jpg", "bio": "Nice to meet you!", "social_links": "@alicesmith",
        "created_at": datetime(2025, 3, 3), "updated_at": datetime(2025, 3, 5)
    }

    created_profile = ProfileMapper.create_profile(data=data, db_session=mock_db_session)

    assert created_profile == 3


def test_update_profile(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1
    data = {
        "bio": "Updated bio",
        "phone_number": "555-987-6543"
    }

    rows_updated = ProfileMapper.update_profile(profile_id=1, data=data, db_session=mock_db_session)

    assert rows_updated == 1


def test_delete_profile(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1

    rows_deleted = ProfileMapper.delete_profile(user_id=1, db_session=mock_db_session)

    assert rows_deleted == 1


def test_create_profile_missing_fields(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
        "user_id": 30, "first_name": "Alice", "last_name": "Johnson", "date_of_birth": datetime(1992, 3, 15),
        "phone_number": "123456789", "address": "789 Boulevard", "city": "Metropolis", "state": "State", "country": "Country",
        "profile_picture": "profile_pic_url", "bio": "Welcome!", "social_links": "https://social3.com", 
        "created_at": datetime(2024, 3, 15), "updated_at": datetime(2024, 3, 15)
    }

    del data["address"]

    with pytest.raises(expected_exception=TypeError):
        ProfileMapper.create_profile(data=data, db_session=mock_db_session)


def test_get_profile_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.side_effect = Exception("Database error")

    with pytest.raises(expected_exception=Exception, match="Database error"):
        ProfileMapper.get_profile(user_id=10, db_session=mock_db_session)


def test_create_profile_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.execute.side_effect = Exception("Database error")
    data = {
        "user_id": 30, "first_name": "Alice", "last_name": "Johnson", "date_of_birth": datetime(1992, 3, 15),
        "phone_number": "123456789", "address": "789 Boulevard", "city": "Metropolis", "state": "State", "country": "Country",
        "profile_picture": "profile_pic_url", "bio": "Welcome!", "social_links": "https://social3.com", 
        "created_at": datetime(2024, 3, 15), "updated_at": datetime(2024, 3, 15)
    }

    with pytest.raises(expected_exception=Exception, match="Database error"):
        ProfileMapper.create_profile(data=data, db_session=mock_db_session)


def test_update_profile_invalid_id(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 0  # Simulate no rows were updated

    data = {
        "phone_number": "111222333", "address": "New Address"
    }

    rows_updated = ProfileMapper.update_profile(profile_id=999, data=data, db_session=mock_db_session)  # Invalid ID

    assert rows_updated == 0  # Expecting no rows to be updated


def test_delete_profile_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.execute.side_effect = Exception("Database error")

    with pytest.raises(expected_exception=Exception, match="Database error"):
        ProfileMapper.delete_profile(user_id=10, db_session=mock_db_session)