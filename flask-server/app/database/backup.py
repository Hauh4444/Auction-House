from datetime import datetime
import sqlite3, os, gzip

DB_DIRECTORY = os.path.join(os.getcwd(), "instance")  # Flask's instance directory
BACKUP_DIRECTORY = os.path.join(DB_DIRECTORY, "backups")  # New folder for backups
DB_FILE = "auctionhouse.db"


def backup_db():
    """
    Creates a compressed backup of the SQLite database by exporting its contents
    into a `.sql.gz` file.
    """
    try:
        os.makedirs(BACKUP_DIRECTORY, exist_ok=True)

        today = datetime.now().strftime("%Y-%m-%d")
        backup_file = f"auctionhouse_backup_{today}.sql.gz"

        db_path = os.path.join(DB_DIRECTORY, DB_FILE)
        backup_path = os.path.join(BACKUP_DIRECTORY, backup_file)

        if not os.path.exists(db_path):
            return

        conn = sqlite3.connect(db_path)

        with gzip.open(backup_path, "wt", encoding="utf-8") as f:  # Compress output
            for line in conn.iterdump():
                f.write(f"{line}\n")
        conn.close()

    except FileNotFoundError as e:
        print(f"File error during backup: {e}")
    except sqlite3.Error as e:
        print(f"SQLite error during backup: {e}")
    except gzip.GzipFile as e:
        print(f"Gzip compression error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during backup: {e}")


def recover_db():
    """
    Recovers the SQLite database from the most recent `.sql.gz` backup file.
    """
    try:
        db_path = os.path.join(DB_DIRECTORY, DB_FILE)

        # Get full paths of backup files from the 'backups' directory
        backup_files = [
            os.path.join(BACKUP_DIRECTORY, f)
            for f in os.listdir(BACKUP_DIRECTORY)
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
