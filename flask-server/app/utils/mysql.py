from flaskext.mysql import MySQL

from .logger import setup_logger

logger = setup_logger(name="app_logger", log_file="logs/app.log")


try:
    # Initialize MySQL
    mysql = MySQL()
except Exception as e:
    # Log any errors during MySQL initialization
    logger.critical(msg=f"MySQL initialization error: {e}")