from flask import jsonify, session, Response

from datetime import datetime, timedelta
import uuid

from ..data_mappers import SessionMapper

logger = setup_logger(name="session_logger", log_file="logs/session.log")

class SessionService:
    """
    TODO:
        We are not currently using this due to issues with race conditions that weren't able to be solved
        This isn't entirely necessary since we are storing session data via the filesystem
        Ideally we would migrate session management/storage to something like redis
    """
    @staticmethod
    def create_session(db_session=None):
        """
        Creates a new user session.

        Args:
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object confirming session creation along with the session ID.
        """
        session_data = {
            "user_id": session.get("user_id"),
            "token": session.get("id"),
            "role": session.get("role"),
            "expires_at": datetime.now() + timedelta(days=1),
        }
        session_id = SessionMapper.create_session(data=session_data, db_session=db_session)
        if not session_id:
            response_data = {"error": "Error creating session"}
            logger.error(msg=f"Failed creating session with data: {', '.join(f'{k}={v!r}' for k, v in session_data.items())}")
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

        response_data = {"message": "Session created", "session_id": session_id}
        logger.info(msg=f"Session: {session_id} created successfully with data: {', '.join(f'{k}={v!r}' for k, v in session_data.items())}")
        return Response(response=jsonify(response_data).get_data(), status=201, mimetype="application/json")
