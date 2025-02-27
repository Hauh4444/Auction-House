import pytest
from unittest.mock import MagicMock

from app.data_mappers.category_mapper import CategoryMapper


# Fixture for a mock database session
@pytest.fixture
def mock_db_session():
    session = MagicMock()
    # Mock the cursor and its behavior
    cursor = MagicMock()
    session.cursor.return_value = cursor
    return session


def test_get_category(mock_db_session):
    # Mock the cursor's execute and fetchone behavior
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.return_value = {
        'category_id': 5,
        'name': 'Electronics',
        'description': 'Electronics'
    }

    # Call the method you are testing
    category = CategoryMapper.get_category_by_id(category_id=5, db_session=mock_db_session)

    assert category is not None
    assert category["category_id"] == 5
    assert category["name"] == "Electronics"
    assert category["description"] == "Electronics"
