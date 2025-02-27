import pytest
from unittest.mock import MagicMock

from datetime import datetime

from app.entities.category import Category


@pytest.fixture
def mock_db_session():
    session = MagicMock()
    return session


def test_category_creation():
    category = Category(
        name="Electronics",
        description="Gadgets and devices"
    )

    assert category.name == "Electronics"
    assert category.description == "Gadgets and devices"
    assert isinstance(category.created_at, str)
    assert isinstance(category.updated_at, str)


def test_category_with_optional_fields():
    category = Category(
        name="Books",
        description="Various books",
        image_encoded="image_data",
        created_at=datetime(2024, 1, 1, 10, 0, 0),
        updated_at=datetime(2024, 1, 2, 12, 0, 0),
        category_id=1
    )

    assert category.category_id == 1
    assert category.image_encoded == "image_data"
    assert category.created_at == datetime(2024, 1, 1, 10, 0, 0)
    assert category.updated_at == datetime(2024, 1, 2, 12, 0, 0)


def test_category_to_dict():
    category = Category(
        name="Furniture",
        description="Home furniture"
    )

    category_dict = category.to_dict()

    assert category_dict["name"] == "Furniture"
    assert category_dict["description"] == "Home furniture"
    assert isinstance(category_dict["created_at"], str)
    assert isinstance(category_dict["updated_at"], str)


def test_category_missing_required_fields():
    with pytest.raises(TypeError):
        Category()


def test_category_invalid_types():
    with pytest.raises(TypeError):
        Category(name=123, description=True)