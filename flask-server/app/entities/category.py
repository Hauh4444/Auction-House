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
        # Type checks
        if not isinstance(name, str):
            raise TypeError(f"name must be a str, got {type(name).__name__}")
        if not isinstance(description, str):
            raise TypeError(f"description must be a str, got {type(description).__name__}")

        if image_encoded is not None and not isinstance(image_encoded, str):
            raise TypeError(f"image_encoded must be a str or None, got {type(image_encoded).__name__}")
        if created_at is not None and not isinstance(created_at, datetime):
            raise TypeError(f"created_at must be a datetime, or None, got {type(created_at).__name__}")
        if updated_at is not None and not isinstance(updated_at, datetime):
            raise TypeError(f"updated_at must be a datetime, or None, got {type(updated_at).__name__}")
        if category_id is not None and not isinstance(category_id, int):
            raise TypeError(f"category_id must be an int or None, got {type(category_id).__name__}")

        self.category_id = category_id
        self.name = name
        self.description = description
        self.image_encoded = image_encoded
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

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

