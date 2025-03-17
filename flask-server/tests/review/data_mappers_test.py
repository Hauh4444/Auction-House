import pytest
from unittest.mock import MagicMock
from datetime import datetime

from app.data_mappers import ReviewMapper


@pytest.fixture
def mock_db_session():
    session = MagicMock()
    session.cursor.return_value = session
    return session


def test_get_all_reviews(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchall.return_value = [
        {
            "review_id": 1, "listing_id": 101, "user_id": 1, "username": "JohnDoe",
            "title": "Great place!", "description": "Loved the experience.", "stars": 5,
            "created_at": datetime(2024, 1, 1)
        },
        {
            "review_id": 2, "listing_id": 102, "user_id": 2, "username": "JaneDoe",
            "title": "Not bad", "description": "It was okay.", "stars": 3,
            "created_at": datetime(2024, 2, 1)
        }
    ]
    
    args = {"listing_id": 101}
    reviews = ReviewMapper.get_all_reviews(args=args, db_session=mock_db_session)
    
    assert len(reviews) == 2
    assert reviews[0]["username"] == "JohnDoe"
    assert reviews[1]["username"] == "JaneDoe"
    assert isinstance(reviews[0]["created_at"], datetime)


def test_get_review_by_id(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.return_value = {
        "review_id": 1, "listing_id": 101, "user_id": 1, "username": "JohnDoe",
        "title": "Great place!", "description": "Loved the experience.", "stars": 5,
        "created_at": datetime(2024, 1, 1)
    }

    review = ReviewMapper.get_review_by_id(review_id=1, db_session=mock_db_session)

    assert review["review_id"] == 1
    assert review["username"] == "JohnDoe"


def test_create_review(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
        "listing_id": 103, "user_id": 3, "username": "AliceSmith",
        "title": "Amazing!", "description": "Had a wonderful time.", "stars": 5,
        "created_at": datetime(2025, 3, 3)
    }

    created_review = ReviewMapper.create_review(data=data, db_session=mock_db_session)

    assert created_review == 3


def test_update_review(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1
    data = {
        "title": "Updated Title",
        "stars": 4
    }

    rows_updated = ReviewMapper.update_review(review_id=1, data=data, db_session=mock_db_session)

    assert rows_updated == 1


def test_delete_review(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1

    rows_deleted = ReviewMapper.delete_review(review_id=1, db_session=mock_db_session)

    assert rows_deleted == 1