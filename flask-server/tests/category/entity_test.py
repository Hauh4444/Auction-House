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
        name="Books",
        description="Various books",
    )

    assert category.name == "Books"
    assert category.description == "Various books"
    assert isinstance(category.name, str)
    assert isinstance(category.description, str)
    assert isinstance(category.created_at, datetime)
    assert isinstance(category.updated_at, datetime)


def test_category_with_optional_fields():
    category = Category(
        category_id=1,
        name="Books",
        description="Various books",
        image_encoded="image_data",
        created_at=datetime(2024, 1, 1, 10, 0, 0),
        updated_at=datetime(2024, 1, 2, 12, 0, 0)
    )

    assert category.category_id == 1
    assert category.image_encoded == "image_data"
    assert category.created_at == datetime(2024, 1, 1, 10, 0, 0)
    assert category.updated_at == datetime(2024, 1, 2, 12, 0, 0)
    assert isinstance(category.category_id, int)
    assert isinstance(category.image_encoded, str)
    assert isinstance(category.created_at, datetime)
    assert isinstance(category.updated_at, datetime)


def test_category_to_dict():
    category = Category(
        category_id=1,
        name="Books",
        description="Various books",
        image_encoded="image_data",
        created_at=datetime(2024, 1, 1, 10, 0, 0),
        updated_at=datetime(2024, 1, 2, 12, 0, 0)
    )

    category_dict = category.to_dict()

    assert category_dict["category_id"] == 1
    assert category_dict["name"] == "Books"
    assert category_dict["description"] == "Various books"
    assert category_dict["image_encoded"] == "image_data"
    assert category_dict["created_at"] == datetime(2024, 1, 1, 10, 0, 0)
    assert category_dict["updated_at"] == datetime(2024, 1, 2, 12, 0, 0)
    assert isinstance(category_dict["category_id"], int)
    assert isinstance(category_dict["name"], str)
    assert isinstance(category_dict["description"], str)
    assert isinstance(category_dict["image_encoded"], str)
    assert isinstance(category_dict["created_at"], datetime)
    assert isinstance(category_dict["updated_at"], datetime)


# noinspection PyArgumentList
def test_category_missing_required_fields():
    with pytest.raises(expected_exception=TypeError):
        Category()


# noinspection PyTypeChecker
def test_category_invalid_types():
    with pytest.raises(expected_exception=TypeError):
        Category(
            category_id="1",
            name=1,
            description=1,
            image_encoded=1,
            created_at=1,
            updated_at=1
        )