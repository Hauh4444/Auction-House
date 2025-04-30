from datetime import datetime


class Session:
    """
    Represents a session in the system.

    Attributes:
        session_id (int, optional): The unique identifier for the session.
        user_id (int): The unique identifier of the user for the session.
        role (str): The role of the user.
        token (str): The unique token of the session used for authenticating the session.
        expires_at (datetime): The timestamp of when the session token expires.
        created_at (datetime): The creation timestamp.
    """
    def __init__(
            self,
            user_id: int,
            role: str,
            token: str,
            expires_at: datetime,
            created_at: datetime | None = None,
            session_id: int | None = None
    ):
        # Type checks for required attributes
        if not isinstance(user_id, int):
            raise TypeError(f"user_id must be a int, got {type(user_id).__name__}")
        if not isinstance(role, str):
            raise TypeError(f"role must be a str, got {type(role).__name__}")
        if not isinstance(token, str):
            raise TypeError(f"token must be a str, got {type(token).__name__}")
        if not isinstance(expires_at, (datetime, str)):
            raise TypeError(f"expires_at must be a datetime, or str, got {type(expires_at).__name__}")

        # Type checks for optional attributes
        if created_at is not None and not isinstance(created_at, (datetime, str)):
            raise TypeError(f"created_at must be a datetime or None, got {type(created_at).__name__}")
        if session_id is not None and not isinstance(session_id, int):
            raise TypeError(f"session_id must be a int or None, got {type(session_id).__name__}")

        self.session_id = session_id
        self.user_id = user_id
        self.role = role
        self.token = token
        self.created_at = created_at or datetime.now()
        self.expires_at = expires_at

    def to_dict(self):
        """Converts the session object to a dictionary representation."""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "role": self.role,
            "token": self.token,
            "created_at": self.created_at,
            "expires_at": self.expires_at
        }