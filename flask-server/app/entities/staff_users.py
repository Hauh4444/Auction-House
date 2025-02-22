from dataclasses import dataclass
from datetime import datetime

@dataclass
class StaffUser:
    """
    Represents a staff user in the system.

    Attributes:
        staff_id (int): The unique identifier for the staff user.
        name (str): The name of the staff user.
        email (str): The email address of the staff user.
        phone (str): The phone number of the staff user.
        role (str): The role of the staff user (e.g., admin, user).
        password_hash (str): The hashed password for the staff user.
        status (str): The current status of the staff user (e.g., active, inactive).
        created_at (datetime, optional): The timestamp for when the user was created.
        updated_at (datetime, optional): The timestamp for the last update to the user.
    """
    def __init__(
            self,
            staff_id: int,
            name: str,
            email: str,
            phone: str,
            role: str,
            password_hash: str,
            status: str,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
    ):
        self.staff_id = staff_id
        self.name = name
        self.email = email
        self.phone = phone
        self.role = role
        self.password_hash = password_hash
        self.status = status
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = updated_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """Converts the user object to a dictionary representation."""
        return {
            "staff_id": self.staff_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
            "password_hash": self.password_hash,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }