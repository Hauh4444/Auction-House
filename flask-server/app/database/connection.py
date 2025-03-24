import sqlite3
import os
from .backup import recover_db

DB_DIRECTORY = "database"
DB_FILE = "auctionhouse.db"


def get_db():
    """
    Establishes a connection to the SQLite database. If the database file is missing,
    it attempts to recover it from the latest backup.

    Returns:
        sqlite3.Connection: A database connection object if successful.
    """
    db_path = os.path.join(DB_DIRECTORY, DB_FILE)

    if not os.path.exists(db_path):  # Check if DB file is missing
        recover_db()

    conn = sqlite3.connect(database=db_path)
    conn.row_factory = sqlite3.Row  # Enables row access by column name
    return conn
