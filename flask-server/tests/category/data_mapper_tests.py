import pytest
from unittest.mock import MagicMock
from ...app.entities.category import Category
from ...app.data_mappers.category_mapper import CategoryMapper


# Fixture for a mock database session
@pytest.fixture
def mock_db_session():
    session = MagicMock()
    return session


# Test CategoryMapper (Mocked Database Interaction)
def test_category_mapper(mock_db_session):
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = Category(
        category_id=5,
        name="Electronics",
        description="Electronics"
    )

    # No need to instantiate CategoryMapper
    category = CategoryMapper.get_category_by_id(5)

    assert category is not None
    assert category["category_id"] == 5
    assert category["name"] == "Electronics"