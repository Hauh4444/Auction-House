from flask_login import LoginManager

from ..data_mappers import AuthMapper
from ..entities import User

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id, db_session=None):
    """
    Loads a user by their ID for Flask-Login session management.

    Args:
        user_id (int): The user ID.
        db_session: Optional database session to be used in tests.

    Returns:
        User: A User object if found, else None.
    """
    user_data = AuthMapper.get_user_by_id(user_id=user_id, db_session=db_session)
    if isinstance(user_data, dict):
        return User(**user_data)
    return user_data