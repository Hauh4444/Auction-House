from flask_login import UserMixin

from dataclasses import dataclass
from datetime import datetime

from ..database import get_db

@dataclass
class StaffUser(UserMixin):
    """
    Represents a staff user in the system.

    Attributes:
        staff_id (int): The unique identifier for the staff user.
        username (str): The username of the user.
        password_hash (str): The hashed password for the staff user.
        name (str): The name of the staff user.
        email (str): The email address of the staff user.
        phone (str): The phone number of the staff user.
        role (str): The role of the staff user (e.g., admin, user).
        status (str): The current status of the staff user (e.g., active, inactive).
        created_at (datetime, optional): The timestamp for when the user was created.
        updated_at (datetime, optional): The timestamp for the last update to the user.
        last_login (datetime, optional): The last login timestamp.
        is_active (bool): Indicates if the user account is active.
    """
    def __init__(
            self,
            staff_id: int,
            username: str,
            password_hash: str,
            name: str,
            email: str,
            phone: str,
            role: str,
            status: str,
            is_active: bool,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
            last_login: datetime | None = None,
    ):
        self.staff_id = staff_id
        self.username = username
        self.password_hash = password_hash
        self.name = name
        self.email = email
        self.phone = phone
        self.role = role
        self.status = status
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = updated_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_login = last_login or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.is_active = bool(is_active)

    def to_dict(self):
        """Converts the user object to a dictionary representation."""
        return {
            "staff_id": self.staff_id,
            "username": self.username,
            "password_hash": self.password_hash,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "last_login": self.last_login,
            "is_active": self.is_active
        }

    @property
    def id(self):
        return self.staff_id

    @property
    def username(self):
        return self._username

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        self._is_active = bool(value)
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE staff_users SET is_active = ? WHERE staff_id = ?", (int(value), self.staff_id))
        db.commit()

    @username.setter
    def username(self, new_username):
        if not new_username or len(new_username) < 3:
            raise ValueError("Username must be at least 3 characters long.")

        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE staff_users SET username = ? WHERE staff_id = ?", (new_username, self.staff_id))
        db.commit()

        self._username = new_username