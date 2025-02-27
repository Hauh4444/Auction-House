import pytest
from unittest.mock import MagicMock
from datetime import datetime

from app.data_mappers.category_mapper import CategoryMapper


@pytest.fixture
def mock_db_session():
    session = MagicMock()
    session.cursor.return_value = session
    return session


def test_get_all_categories(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchall.return_value = [
        {
            "category_id": 1,
            "name": "Electronics",
            "description": "Gadgets and devices",
            "image_encoded": "image1",
            "created_at": datetime(2023, 1, 1, 12, 0, 0),
            "updated_at": datetime(2023, 1, 2, 12, 0, 0)
        },
        {
            "category_id": 2,
            "name": "Books",
            "description": "Various books",
            "image_encoded": "image2",
            "created_at": datetime(2023, 2, 1, 12, 0, 0),
            "updated_at": datetime(2023, 2, 2, 12, 0, 0)
        }
    ]

    categories = CategoryMapper.get_all_categories(db_session=mock_db_session)

    assert len(categories) == 2
    assert categories[0]["name"] == "Electronics"
    assert isinstance(categories[0]["created_at"], datetime)
    assert isinstance(categories[0]["updated_at"], datetime)


def test_get_category(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.return_value = {
        "category_id": 1,
        "name": "Electronics",
        "description": "Gadgets and devices",
        "image_encoded": "image1",
        "created_at": datetime(2023, 1, 1, 12, 0, 0),
        "updated_at": datetime(2023, 1, 2, 12, 0, 0)
    }

    category = CategoryMapper.get_category_by_id(1, db_session=mock_db_session)

    assert category["category_id"] == 1
    assert category["name"] == "Electronics"
    assert isinstance(category["created_at"], datetime)
    assert isinstance(category["updated_at"], datetime)


def test_create_category(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
        "name": "Furniture",
        "description": "Home furniture",
        "image_encoded": "image3",
        "created_at": datetime(2023, 3, 1, 12, 0, 0),
        "updated_at": datetime(2023, 3, 2, 12, 0, 0)
    }

    category_id = CategoryMapper.create_category(data, db_session=mock_db_session)

    assert category_id == 3


def test_update_category(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1
    data = {
        "name": "Updated Electronics",
        "description": "Updated gadgets"
    }

    rows_updated = CategoryMapper.update_category(1, data, db_session=mock_db_session)

    assert rows_updated == 1


def test_delete_category(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1

    rows_deleted = CategoryMapper.delete_category(1, db_session=mock_db_session)

    assert rows_deleted == 1


# Test for missing required fields in creating a category
def test_create_category_missing_fields(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
        "name": "Furniture",
        "description": "Home furniture",
        "image_encoded": "image3",
        "created_at": datetime(2023, 3, 1, 12, 0, 0),
        "updated_at": datetime(2023, 3, 2, 12, 0, 0)
    }

    # Missing name (required field)
    del data["name"]

    with pytest.raises(TypeError):
        CategoryMapper.create_category(data, db_session=mock_db_session)


# Test for invalid data types
def test_create_category_invalid_data_type(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
        "name": "Furniture",
        "description": "Home furniture",
        "image_encoded": "image3",
        "created_at": datetime(2023, 3, 1, 12, 0, 0),
        "updated_at": datetime(2023, 3, 2, 12, 0, 0)
    }

    # Invalid type for created_at, should be datetime
    data["created_at"] = 2023

    with pytest.raises(TypeError):
        CategoryMapper.create_category(data, db_session=mock_db_session)


# Test for database failure when fetching category by id
def test_get_category_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        CategoryMapper.get_category_by_id(1, db_session=mock_db_session)


# Test for no categories returned when fetching all categories
def test_get_all_categories_no_results(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchall.return_value = []

    categories = CategoryMapper.get_all_categories(db_session=mock_db_session)

    assert len(categories) == 0


# Test for database failure when creating a category
def test_create_category_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.execute.side_effect = Exception("Database error")

    data = {
        "name": "Furniture",
        "description": "Home furniture",
        "image_encoded": "image3",
        "created_at": datetime(2023, 3, 1, 12, 0, 0),
        "updated_at": datetime(2023, 3, 2, 12, 0, 0)
    }

    with pytest.raises(Exception, match="Database error"):
        CategoryMapper.create_category(data, db_session=mock_db_session)


# Test for invalid category id during update
def test_update_category_invalid_id(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 0  # Simulate no rows were updated

    data = {
        "name": "Updated Electronics",
        "description": "Updated gadgets"
    }

    rows_updated = CategoryMapper.update_category(999, data, db_session=mock_db_session)  # Invalid ID

    assert rows_updated == 0  # Expecting no rows to be updated


# Test for database failure when deleting a category
def test_delete_category_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.execute.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        CategoryMapper.delete_category(1, db_session=mock_db_session)

