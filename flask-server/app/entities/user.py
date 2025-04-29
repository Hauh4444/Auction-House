from flask_login import UserMixin

from pymysql import cursors
from datetime import datetime

from ..database import get_db


class User(UserMixin):
    """
    Represents a user in the system.

    Attributes:
        user_id (int): The unique identifier for the user.
        role (str): The role of the user.
        username (str): The username of the user.
        password_hash (str): The hashed password.
        email (str): The email address of the user.
        created_at (datetime, optional): The timestamp when the user was created.
        updated_at (datetime, optional): The timestamp when the user was last updated.
        last_login (datetime, optional): The last login timestamp.
        is_active (bool): Indicates if the user account is active.
        db_session: Optional database session for tests
    """
    def __init__(
        self,
        role: str,
        username: str,
        password_hash: str,
        email: str,
        db_session=None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        last_login: datetime | None = None,
        is_active: bool | None = None,
        user_id: int | None = None,
    ):
        self.db_session = db_session
        self.user_id = user_id
        self.username = username
        self.role = role
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
            "role": self.role,
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

    @username.setter
    def username(self, value):
        if not isinstance(value, str):
            raise TypeError(f"username must be a str, got {type(value).__name__}")
        if not value or len(value) < 3:
            raise ValueError(f"username must be of length 3 got '{value}' instead")

        self._username = value

        if self.user_id is not None:
            db = get_db()
            cursor = db.cursor(cursors.DictCursor)  # type: ignore
            cursor.execute("UPDATE users SET username = %s WHERE user_id = %s", (value, self.user_id))
            db.commit()

    @is_active.setter
    def is_active(self, value):
        if not isinstance(value, int) and not isinstance(value, bool):
            raise TypeError(f"is_active must be a int or bool, got '{type(value).__name__}'")

        self._is_active = bool(value)

        if self.user_id is not None:
            db = self.db_session or get_db()
            cursor = db.cursor(cursors.DictCursor) # type: ignore
            cursor.execute("UPDATE users SET is_active = %s WHERE user_id = %s", (int(value), self.user_id))
            db.commit()