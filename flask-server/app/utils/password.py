import hashlib

from .logger import setup_logger

logger = setup_logger(name="app_logger", log_file="logs/app.log")


def hash_password(password: str):
    """
    Hashes the password using SHA256.

    Args:
        password (str): The password to hash.

    Returns:
        str: A hashed version of the password.
    """
    try:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password
    except Exception as e:
        # Log any errors during the hashing process
        logger.error(f"Error hashing password: {e}")
        raise