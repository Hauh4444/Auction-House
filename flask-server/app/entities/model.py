from datetime import datetime


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
            listing_id: int,
            file_reference: str,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
            model_id: int | None = None
    ):
        # Type checks for required attributes
        if not isinstance(listing_id, int):
            raise TypeError(f"listing_id must be an int, got {type(listing_id).__name__}")
        if not isinstance(file_reference, str):
            raise TypeError(f"file_reference must be a str, got {type(file_reference).__name__}")

        self.model_id = model_id
        self.listing_id = listing_id
        self.file_reference = file_reference
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        """Converts the model object to a dictionary representation."""
        return {
            "model_id": self.model_id,
            "listing_id": self.listing_id,
            "file_reference": self.file_reference,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }