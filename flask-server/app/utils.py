from flask import send_file
from flask_login import LoginManager
import sqlite3, os, threading, time
from .data_mappers.user_login_mapper import UserMapper
from .entities.user import User

login_manager = LoginManager()

db_name = "./database/auctionhouse.db"
backup_file = "./database/auctionhouse_backup.sql"

@login_manager.user_loader
def load_user(user_id):
    """
    Loads a user by their ID for Flask-Login session management.

    Args:
        user_id (int): The user ID.

    Returns:
        User: A User object if found, else None.
    """
    user_data = UserMapper.get_user_by_id(user_id)
    if isinstance(user_data, dict):
        return User(**user_data)
    return user_data

def backup_database():
    """
    Creates a backup of the SQLite database by exporting its contents.

    Returns:
        str: A success message if the backup is created successfully.
        tuple: An error message and HTTP status code if the database file is not found.
    """
    try:
        if not os.path.exists(db_name):
            return "Database file not found!", 404

        conn = sqlite3.connect(db_name)
        with open(backup_file, "w") as f:
            for line in conn.iterdump():
                f.write(f"{line}\n")
        conn.close()

        return "Database backup created successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def scheduled_backup():
    """
    Runs an infinite loop that triggers the database backup process every 12 hours.
    """
    while True:
        backup_database()
        time.sleep(12 * 60 * 60) # Sleep for 12 hours

def start_scheduled_backup():
    """
    Starts the scheduled database backup process in a separate daemon thread.
    """
    threading.Thread(target=scheduled_backup, daemon=True).start()

def download_backup():
    """
    Allows users to download the most recent database backup file.

    Returns:
        Flask response: The backup file as an attachment if found.
        tuple: An error message and HTTP status code if the backup file is not found.
    """
    if not os.path.exists(backup_file):
        return "Backup file not found!", 404
    return send_file(backup_file, as_attachment=True)
