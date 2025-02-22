from flask import send_file
import redis
import sqlite3
import os
import threading
import time

db_name = "./database/auctionhouse.db"
backup_file = "./database/auctionhouse_backup.sql"


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