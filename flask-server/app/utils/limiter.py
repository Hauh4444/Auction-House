from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from .logger import setup_logger

logger = setup_logger(name="app_logger", log_file="logs/app.log")


try:
    # Initialize limiter
    limiter = Limiter(
        get_remote_address,
        default_limits=["10000 per hour", "2000 per minute"],
        storage_uri="memory://"
    )
except Exception as e:
    # Log any errors during limiter initialization
    logger.warning(msg=f"Limiter initialization error: {e}")