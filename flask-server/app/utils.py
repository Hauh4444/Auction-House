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
        User object if found, else None.
    """
    user_data = UserMapper.get_user_by_id(user_id)  # Ensure this returns a User instance

    # If `user_data` is a dictionary, convert it to a `User` object
    if isinstance(user_data, dict):
        return User(**user_data)  # Convert dictionary to User object

    return user_data


def backup_database():
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
    while True:
        backup_database()
        time.sleep(12 * 60 * 60)  # Sleep for 12 hours


def start_scheduled_backup():
    threading.Thread(target=scheduled_backup, daemon=True).start()


def download_backup():
    if not os.path.exists(backup_file):
        return "backup file not found!", 404
    return send_file(backup_file, as_attachment=True)