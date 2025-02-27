from dataclasses import dataclass
from datetime import datetime


@dataclass
class Category:
    """
    Represents a category in the system.

    Attributes:
        category_id (int, optional): The unique identifier for the category.
        name (str): The name of the category.
        description (str): The description of the category.
        image_encoded (str, optional): Encoded image data for the category.
        created_at (datetime, optional): The creation timestamp.
        updated_at (datetime, optional): The last updated timestamp.
    """
    def __init__(
            self,
            name: str,
            description: str,
            image_encoded: str | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
            category_id: int | None = None
    ):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not isinstance(description, str):
            raise TypeError("description must be a string")
        if image_encoded is not None and not isinstance(image_encoded, str):
            raise TypeError("image_encoded must be a string or None")
        if created_at is not None and not isinstance(created_at, datetime) and not isinstance(created_at, str):
            raise TypeError("created_at must be a datetime or None")
        if updated_at is not None and not isinstance(updated_at, datetime) and not isinstance(created_at, str):
            raise TypeError("updated_at must be a datetime or None")
        if category_id is not None and not isinstance(category_id, int):
            raise TypeError("category_id must be an int or None")

        self.category_id = category_id
        self.name = name
        self.description = description
        self.image_encoded = image_encoded
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = updated_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """Converts the category object to a dictionary representation."""
        return {
            "category_id": self.category_id,
            "name": self.name,
            "description": self.description,
            "image_encoded": self.image_encoded,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

