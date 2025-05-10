from mysql.connector import Error
from dotenv import load_dotenv
import os, pymysql

from ..utils.mysql import mysql
from ..utils.logger import setup_logger
from .backup import recover_db

load_dotenv()

logger = setup_logger(name="database_logger", log_file="logs/database.log")


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
        logger.info(msg=f"Database: {os.getenv('DB')} successfully connected")
        return conn

    except Error as e:
        if e.errno == 1049:  # Error code for "Unknown database"
            recover_db()  # Recover the database from backup
            conn = mysql.connect()
            conn.cursor().execute(f"USE {os.getenv('DB')}")  # Retry selecting the database
            logger.info(msg=f"Database: {os.getenv('DB')} successfully connected after backup recovery")
            return conn
        else:
            logger.critical(msg=f"MySQL Connection Error: {e}")
            return None
