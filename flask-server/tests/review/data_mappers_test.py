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


def test_create_review_missing_fields(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
        "review_id": 1, "listing_id": 101, "user_id": 1, "username": "JohnDoe",
        "title": "Great place!", "description": "Loved the experience.", "stars": 5,
        "created_at": datetime(2024, 1, 1)
           }

    del data["description"]

    with pytest.raises(expected_exception=TypeError):
        ReviewMapper.create_review(data=data, db_session=mock_db_session)


def test_get_review_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.side_effect = Exception("Database error")

    with pytest.raises(expected_exception=Exception, match="Database error"):
        ReviewMapper.get_review_by_id(review_id=1, db_session=mock_db_session)


def test_create_review_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.execute.side_effect = Exception("Database error")
    data = {
        "listing_id": 200, "user_id": 30, "username": "alice_jones", "title": "Amazing Experience", 
        "description": "I had a great time!", "stars": 5, "created_at": datetime(2024, 3, 1)
    }

    with pytest.raises(expected_exception=Exception, match="Database error"):
        ReviewMapper.create_review(data=data, db_session=mock_db_session)


def test_update_review_invalid_id(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 0  # Simulate no rows were updated

    data = {
        "title": "Updated Title", "description": "Updated Description", "stars": 4
    }

    rows_updated = ReviewMapper.update_review(review_id=999, data=data, db_session=mock_db_session)  # Invalid ID

    assert rows_updated == 0  # Expecting no rows to be updated


def test_delete_review_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.execute.side_effect = Exception("Database error")

    with pytest.raises(expected_exception=Exception, match="Database error"):
        ReviewMapper.delete_review(review_id=1, db_session=mock_db_session)