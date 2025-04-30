from flask_login import LoginManager
from ..data_mappers import AuthMapper
from ..entities import User
from .logger import setup_logger

logger = setup_logger(name="app_logger", log_file="logs/app.log")

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id: int):
    """
    Loads a user by their ID for Flask-Login session management.

    Args:
        user_id (int): The user ID.

    Returns:
        User: A User object if found, else None.
    """
    try:
        user_data = AuthMapper.get_user_by_id(user_id=user_id)
        if isinstance(user_data, dict):
            return User(**user_data)
        return user_data
    except Exception as e:
        logger.critical(msg=f"Failed loading user with ID {user_id}: {e}")
        return None
