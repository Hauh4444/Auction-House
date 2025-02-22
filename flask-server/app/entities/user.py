from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    """
    Represents a user in the system.

    Attributes:
        user_id (int): The unique identifier for the user.
        username (str): The username of the user.
        password_hash (str): The hashed password.
        email (str): The email address of the user.
        created_at (datetime, optional): The timestamp when the user was created.
        updated_at (datetime, optional): The timestamp when the user was last updated.
        last_login (datetime, optional): The last login timestamp.
        is_active (bool): Indicates if the user account is active.
    """
    def __init__(
            self,
            user_id: int,
            username: str,
            password_hash: str,
            email: str,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
            last_login: datetime | None = None,
            is_active: bool = True
    ):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = updated_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_login = last_login
        self.is_active = is_active

    def to_dict(self):
        """Converts the user object to a dictionary representation."""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password_hash": self.password_hash,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "last_login": self.last_login.strftime("%Y-%m-%d %H:%M:%S") if self.last_login else None,
            "is_active": self.is_active
        }