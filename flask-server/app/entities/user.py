from flask_login import UserMixin

from pymysql import cursors
from dataclasses import dataclass
from datetime import datetime

from ..database.connection import get_db


@dataclass
class User(UserMixin):
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
            username: str,
            password_hash: str,
            email: str,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
            last_login: datetime | None = None,
            is_active: bool | None = None,
            user_id: int | None = None,
    ):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.last_login = last_login or datetime.now()
        self.is_active = bool(is_active)

    def to_dict(self):
        """Converts the user object to a dictionary representation."""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password_hash": self.password_hash,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "last_login": self.last_login,
            "is_active": self.is_active
        }

    @property
    def id(self):
        return self.user_id

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
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("UPDATE users SET is_active = %s WHERE user_id = %s", (int(value), self.user_id))
        db.commit()

    @username.setter
    def username(self, new_username):
        if not new_username or len(new_username) < 3:
            raise ValueError("Username must be at least 3 characters long.")

        db = get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("UPDATE users SET username = %s WHERE user_id = %s", (new_username, self.user_id))
        db.commit()

        self._username = new_username