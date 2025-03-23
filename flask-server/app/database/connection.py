from mysql.connector import Error
import sqlite3

from ..utils.mysql import mysql
from .backup import recover_db


def get_db():
    """
    Establishes a connection to the SQLite database. If the database file is missing,
    it attempts to recover it from the latest backup.

    Returns:
        sqlite3.Connection: A database connection object if successful.
    """
    try:
        conn = mysql.connect()
        conn.cursor().execute("USE auctionhouse")  # Try selecting the database
        return conn

    except Error as e:
        if e.errno == 1049:  # Error code for "Unknown database"
            recover_db()  # Recover the database from backup
            conn = mysql.connect()
            conn.cursor().execute("USE auctionhouse")  # Retry selecting the database
            return conn
        else:
            print(f"MySQL Connection Error: {e}")
            return None
