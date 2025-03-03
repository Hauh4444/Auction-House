import sqlite3, os

DB_FILE = "database/auctionhouse.db"
BACKUP_FILE = "./database/auctionhouse_backup.sql"


def get_db():
    """Establish a connection to the SQLite database.

    Returns:
        sqlite3.Connection: A database connection object.
    """
    # TODO If we fail to connect to database, call recover_backup() and attempt to connect again
    conn = sqlite3.connect(database=DB_FILE)
    conn.row_factory = sqlite3.Row # Enables row access by column name
    return conn

def backup_database():
    """
    Creates a backup of the SQLite database by exporting its contents.

    Returns:
        str: A success message if the backup is created successfully.
        tuple: An error message and HTTP status code if the database file is not found.
    """
    # TODO Backup files need to be timestamped and not overridden upon new backups
    try:
        if not os.path.exists(path=DB_FILE):
            return "Database file not found!", 404

        conn = sqlite3.connect(database=DB_FILE)
        with open(BACKUP_FILE, "w") as f:
            for line in conn.iterdump():
                f.write(f"{line}\n")
        conn.close()

        return "Database backup created successfully."
    except Exception as e:
        return f"Error: {str(e)}"


def recover_backup():
    # TODO this function will recover the database from the latest backup file, then delete that latest backup file
    return
