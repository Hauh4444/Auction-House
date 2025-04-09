from dataclasses import dataclass
from datetime import datetime


@dataclass
class Model:
    """
    Represents a 3D model in the system.

    Attributes:
        model_id (int, optional): The unique identifier for the model.
        name (str): The name of the 3D model.
        file_reference (str): The file path or reference to the 3D model file.
        file_size (float): The size of the 3D model file in megabytes.
        listing_id (int): The ID of the associated listing.
        created_at (datetime, optional): The timestamp when the model was created.
        updated_at (datetime, optional): The timestamp when the model was last updated.
    """
    def __init__(
            self,
            name: str,
            file_reference: str,
            file_size: float,
            listing_id: int,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
            model_id: int | None = None
    ):
        # Type checks for required attributes
        if not isinstance(name, str):
            raise TypeError(f"name must be a str, got {type(name).__name__}")
        if not isinstance(file_reference, str):
            raise TypeError(f"file_reference must be a str, got {type(file_reference).__name__}")
        if not isinstance(file_size, (int, float)):
            raise TypeError(f"file_size must be a number, got {type(file_size).__name__}")
        if not isinstance(listing_id, int):
            raise TypeError(f"listing_id must be an int, got {type(listing_id).__name__}")

        self.model_id = model_id
        self.name = name
        self.file_reference = file_reference
        self.file_size = file_size
        self.listing_id = listing_id
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        """Converts the model object to a dictionary representation."""
        return {
            "model_id": self.model_id,
            "name": self.name,
            "file_reference": self.file_reference,
            "file_size": self.file_size,
            "listing_id": self.listing_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }