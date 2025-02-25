from flask_login import LoginManager
from .data_mappers.user_login_mapper import UserMapper
from .entities.user import User

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    """
    Loads a user by their ID for Flask-Login session management.

    Args:
        user_id (int): The user ID.

    Returns:
        User object if found, else None.
    """
    user_data = UserMapper.get_user_by_id(user_id)  # Ensure this returns a User instance

    # If `user_data` is a dictionary, convert it to a `User` object
    if isinstance(user_data, dict):
        return User(**user_data)  # Convert dictionary to User object

    return user_data