from dataclasses import dataclass
from datetime import datetime

@dataclass
class Session:
    def __init__(
            self,
            session_id: int,
            user_id: int,
            token: str | None = None,
            created_at: datetime | None = None
    ):
        self.session_id = session_id
        self.user_id = user_id
        self.token = token
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """Converts the session object to a dictionary representation."""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "token": self.token,
            "created_at": self.created_at
        }