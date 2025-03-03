from datetime import datetime
import sqlite3, os, gzip

today = datetime.now().strftime("%Y-%m-%d")
DB_DIRECTORY = "database"
DB_FILE = "auctionhouse.db"
BACKUP_FILE = f"auctionhouse_backup_{today}.sql"


def get_db():
    """
    Establishes a connection to the SQLite database. If the database file is missing,
    it attempts to recover it from the latest backup.

    Returns:
        sqlite3.Connection: A database connection object if successful.
    """
    db_path = os.path.join(DB_DIRECTORY, DB_FILE)

    if not os.path.exists(db_path):  # Check if DB file is missing
        recover_database()

    conn = sqlite3.connect(database=db_path)
    conn.row_factory = sqlite3.Row  # Enables row access by column name
    return conn


def backup_database():
    """
    Creates a compressed backup of the SQLite database by exporting its contents
    into a `.sql.gz` file.
    """
    try:
        os.makedirs(DB_DIRECTORY, exist_ok=True)

        db_path = os.path.join(DB_DIRECTORY, DB_FILE)
        backup_path = os.path.join(DB_DIRECTORY, BACKUP_FILE + ".gz")

        if not os.path.exists(db_path):
            return

        conn = sqlite3.connect(db_path)

        with gzip.open(backup_path, "wt", encoding="utf-8") as f:  # Compress output
            for line in conn.iterdump():
                f.write(f"{line}\n")
        conn.close()

    except FileNotFoundError as e:
        print(f"File error during recovery: {e}")
    except sqlite3.Error as e:
        print(f"SQLite error during recovery: {e}")
    except gzip.GzipFile as e:
        print(f"Gzip decompression error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during recovery: {e}")


def recover_database():
    """
    Recovers the SQLite database from the most recent `.sql.gz` backup file.
    After successful recovery, the backup file is deleted.
    """
    try:
        db_path = os.path.join(DB_DIRECTORY, DB_FILE)

        # Get full paths of backup files
        backup_files = [
            os.path.join(DB_DIRECTORY, f)
            for f in os.listdir(DB_DIRECTORY)
            if f.startswith("auctionhouse_backup_") and f.endswith(".sql.gz")
        ]

        backup_files = sorted(backup_files, key=os.path.getmtime, reverse=True)

        if not backup_files:
            return

        latest_backup = backup_files[0]

        # Restore database from gzip file
        with gzip.open(latest_backup, "rt", encoding="utf-8") as f:
            sql_script = f.read()

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.executescript(sql_script)
            conn.commit()

        # Delete the backup after successful recovery
        os.remove(latest_backup)

    except FileNotFoundError as e:
        print(f"File error during recovery: {e}")
    except sqlite3.Error as e:
        print(f"SQLite error during recovery: {e}")
    except gzip.GzipFile as e:
        print(f"Gzip decompression error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during recovery: {e}")
