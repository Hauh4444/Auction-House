import pytest
from unittest.mock import MagicMock
from ...app.entities.category import Category


# Fixture for a mock database session
@pytest.fixture
def mock_db_session():
    session = MagicMock()
    return session


# Test Category Entity
def test_category_entity():
    category = Category(
        category_id=5,
        name="Electronics",
        description="Electronics"
    )
    assert category.category_id == 5
    assert category.name == "Electronics"