from apscheduler.schedulers.background import BackgroundScheduler

from ..database.backup import backup_db

scheduler = BackgroundScheduler()
scheduler.add_job(backup_db, trigger="cron", hour=12, minute=0)  # Runs every day at Noon