import pytest
from unittest.mock import MagicMock
from datetime import datetime

from app.data_mappers import ProfileMapper


@pytest.fixture
def mock_db_session():
    session = MagicMock()
    session.cursor.return_value = session
    return session


def test_get_profile(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.return_value = {
    "user_id": 1, "first_name": "John", "last_name": "Doe", 
    "date_of_birth": datetime(1990, 1, 1),  # Ensure this is a datetime object
    "phone_number": "123-456-7890", "address": "123 Main St", 
    "city": "New York", "state": "NY", "country": "USA", 
    "profile_picture": "profile1.jpg", "bio": "Hello!", 
    "social_links": {"facebook": "@johndoe"},
    "created_at": datetime(2024, 1, 1), 
    "updated_at": datetime(2024, 1, 3)
}

    profile = ProfileMapper.get_profile(user_id=1, db_session=mock_db_session)

    assert profile["user_id"] == 1
    assert profile["first_name"] == "John"


def test_create_profile(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
    "user_id": 3, "first_name": "Alice", "last_name": "Smith", 
    "date_of_birth": datetime(1995, 3, 3),  # Change string to datetime
    "phone_number": "555-123-4567", "address": "789 Maple St", 
    "city": "Chicago", "state": "IL", "country": "USA", 
    "profile_picture": "profile3.jpg", "bio": "Nice to meet you!", 
    "social_links": {"facebook": "@alicesmith"},
    "created_at": datetime(2025, 3, 3),  # Ensure this is a datetime object
    "updated_at": datetime(2025, 3, 5)   # Ensure this is a datetime object
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
