from flask_session import Session

from .logger import setup_logger

logger = setup_logger(name="app_logger", log_file="logs/app.log")


try:
    # Initialize session
    flask_session = Session()
except Exception as e:
    # Log any errors during session initialization
    logger.warning(msg=f"Session initialization error: {e}")
