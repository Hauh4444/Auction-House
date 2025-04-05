from datetime import datetime
from dotenv import load_dotenv
import os, pymysql
from ..utils.mysql import mysql

load_dotenv()

BACKUP_DIRECTORY = os.path.join(os.getcwd(), "database_backups")


def backup_db():
    """
    Creates a backup of the MySQL database by exporting its structure and data into a `.sql` file.

    This function performs the following tasks:
    1. Creates a backup directory if it does not already exist.
    2. Connects to the MySQL database using the credentials from the environment variables.
    3. Dumps the structure (CREATE TABLE statements) and data (INSERT INTO statements) of each table in the database into a `.sql` file.
    4. Saves the backup file with a timestamped filename in the `database_backups` directory.

    The resulting `.sql` file contains the full schema and data necessary to recreate the database.

    Raises:
        mysql.connector.Error: If there is an error while interacting with the MySQL database.
        Exception: If an unexpected error occurs during the backup process.
    """
    try:
        os.makedirs(BACKUP_DIRECTORY, exist_ok=True)

        today = datetime.now().strftime("%Y-%m-%d")
        backup_file = f"auctionhouse_backup_{today}.sql"
        backup_path = os.path.join(BACKUP_DIRECTORY, backup_file)

        conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB")
        )

        cursor = conn.cursor()

        with open(backup_path, "w", encoding="utf-8") as f:
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]

            for table in tables:
                # Dump table structure
                cursor.execute(f"SHOW CREATE TABLE {table}")
                create_table = cursor.fetchone()[1]
                f.write(f"{create_table};\n\n")

                # Dump table data
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

                for row in rows:
                    values = ', '.join(
                        f"'{str(item).replace('\'', '\\\'')}'" if item is not None else 'NULL' for item in row
                    )
                    f.write(f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({values});\n")
                f.write("\n")

        cursor.close()
        conn.close()
        print(f"Backup successful: {backup_path}")

    except mysql.connector.Error as err:
        print(f"MySQL Error during backup: {err}")
    except Exception as e:
        print(f"Unexpected error during backup: {e}")


def recover_db():
    """
    Restores the MySQL database from the latest `.sql` backup file.

    This function performs the following tasks:
    1. Scans the `database_backups` directory for `.sql` backup files.
    2. Sorts the backup files by modification date to find the most recent backup.
    3. Connects to the MySQL database using the configured credentials.
    4. Reads the SQL script from the latest backup file and executes it to restore the database.
    5. Commits the changes to the database.

    The restoration process will overwrite the current database state with the data from the backup.

    Raises:
        mysql.connector.Error: If there is an error while interacting with the MySQL database during the recovery process.
        Exception: If an unexpected error occurs during the recovery process.
    """
    try:
        backup_files = [
            os.path.join(BACKUP_DIRECTORY, f)
            for f in os.listdir(BACKUP_DIRECTORY)
            if f.startswith("auctionhouse_backup_") and f.endswith(".sql")
        ]
        backup_files = sorted(backup_files, key=os.path.getmtime, reverse=True)

        if not backup_files:
            print("No backup files found.")
            return

        latest_backup = backup_files[0]

        conn = mysql.connector.connect(
            host="localhost",
            user="Preston",
            password="",
            database="auctionhouse"
        )
        cursor = conn.cursor()

        with open(latest_backup, encoding="utf-8") as f:
            sql_script = f.read()

        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)

        conn.commit()
        cursor.close()
        conn.close()
        print(f"Database restored from {latest_backup}")

    except mysql.connector.Error as err:
        print(f"MySQL Error during recovery: {err}")
    except Exception as e:
        print(f"Unexpected error during recovery: {e}")