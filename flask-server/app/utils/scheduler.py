from apscheduler.schedulers.background import BackgroundScheduler

from ..database import backup_db
from .logger import setup_logger

logger = setup_logger(name="app_logger", log_file="logs/app.log")


try:
    # Initialize scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(backup_db, trigger="cron", hour=12, minute=0)  # Runs every day at Noon
except Exception as e:
    # Log any errors during scheduler initialization
    logger.warning(msg=f"Scheduler initialization error: {e}")