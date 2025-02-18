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

