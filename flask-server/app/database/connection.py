from mysql.connector import Error
from dotenv import load_dotenv
import os, pymysql

from ..utils.mysql import mysql
from .backup import recover_db

load_dotenv()


def get_db():
    """
    Establishes a connection to the MySQL database. If the database is missing (Error 1049),
    it attempts to recover it from the latest backup file.

    The function first tries to connect to the MySQL database using the credentials and database
    name from environment variables. If the database is not found (Error 1049: "Unknown database"),
    it invokes the `recover_db` function to restore the database from the most recent backup. After
    recovery, it retries the connection and returns the connection object.

    Returns:
        pymysql.connections.Connection: A connection object to the MySQL database if successful.
        None: If the connection attempt fails due to an error other than "Unknown database".

    Raises:
        Error: If there is a MySQL connection error other than "Unknown database".
    """
    try:
        conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB")
        )
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
