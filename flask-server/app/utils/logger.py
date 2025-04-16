import logging
from logging.handlers import RotatingFileHandler
import os

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

login_logger = logging.getLogger("login_tracker")
login_logger.setLevel(logging.INFO)

log_file = os.path.join(log_dir, "login_activity.log")
handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)

if not login_logger.hasHandlers():
    login_logger.addHandler(handler)
