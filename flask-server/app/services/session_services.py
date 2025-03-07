from flask import jsonify, session, Response

from datetime import datetime, timedelta

from ..data_mappers import SessionMapper


class SessionService:
    @staticmethod
    def create_session(db_session=None):
        """
        Creates a new user session.

        Args:
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object confirming session creation along with the session ID.
        """
        data = {
            "user_id": session["user_id"],
            "token": session["_id"],
            "role": session["role"],
            "expires_at": datetime.now() + timedelta(days=1),
        }
        session_id = SessionMapper.create_session(data=data, db_session=db_session)

        if not session_id:
            data = {"message": "Error creating session"}
            return Response(response=jsonify(data).get_data(), status=400, mimetype="application/json")

        data = {"message": "Session created", "session_id": session_id}
        return Response(response=jsonify(data).get_data(), status=201, mimetype="application/json")
