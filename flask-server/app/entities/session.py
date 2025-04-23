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
            # TODO All datetime instances need to have this check
            "created_at": self.created_at if isinstance(self.created_at, datetime) else self.created_at,
            "expires_at": self.expires_at
        }