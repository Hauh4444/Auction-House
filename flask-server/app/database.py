import sqlite3

DB_FILE = "database/auctionhouse.db"


def get_db():
    """Establish a connection to the SQLite database.

    Returns:
        sqlite3.Connection: A database connection object.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Enables row access by column name
    return conn


def init_db():
    """Initialize the database by creating necessary tables if they don't exist."""
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            image_encoded TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    db.commit()
