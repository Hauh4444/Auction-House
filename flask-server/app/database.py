import sqlite3

DB_FILE = "database/auctionhouse.db"


def get_db():
    """Establish a connection to the SQLite database.

    Returns:
        sqlite3.Connection: A database connection object.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row # Enables row access by column name
    return conn


def init_db():
    """Initialize the database by creating necessary tables if they don't exist."""
    db = get_db()
    cursor = db.cursor()

    tables = [
        """
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            image_encoded TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS chat_messages (
            "message_id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "chat_id" INTEGER NOT NULL,
            "sender_id" INTEGER NOT NULL,
            "message" TEXT NOT NULL,
            "sent_at" DATETIME NOT NULL,
            FOREIGN KEY("chat_id") REFERENCES "chats"("chat_id"),
            FOREIGN KEY("sender_id") REFERENCES "users"("user_id")
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS chats (
            "chat_id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "user1_id" INTEGER NOT NULL,
            "user2_id" INTEGER NOT NULL,
            "created_at" DATETIME NOT NULL,
            "updated_at" DATETIME NOT NULL,
            FOREIGN KEY("user1_id") REFERENCES "users"("user_id"),
            FOREIGN KEY("user2_id") REFERENCES "users"("user_id")
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS deliveries (
            "delivery_id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "order_id" INTEGER NOT NULL,
            "user_id" INTEGER NOT NULL,
            "address" TEXT NOT NULL,
            "city" VARCHAR NOT NULL,
            "state" VARCHAR NOT NULL,
            "postal_code" VARCHAR NOT NULL,
            "country" VARCHAR NOT NULL,
            "delivery_status" VARCHAR NOT NULL,
            "tracking_number" VARCHAR NOT NULL,
            "courier" VARCHAR NOT NULL,
            "estimated_delivery_date" DATE NOT NULL,
            "delivered_at" DATETIME,
            "created_at" DATETIME NOT NULL,
            "updated_at" DATETIME NOT NULL,
            FOREIGN KEY("order_id") REFERENCES "orders"("order_id")
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS listings (
            "listing_id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "user_id" INTEGER NOT NULL,
            "title" VARCHAR NOT NULL,
            "title_short" VARCHAR(20) NOT NULL,
            "description" TEXT NOT NULL,
            "item_specifics" TEXT NOT NULL,
            "category_id" VARCHAR NOT NULL,
            "listing_type" TEXT NOT NULL CHECK("listing_type" IN ('auction', 'buy_now')),
            "starting_price" NUMERIC,
            "reserve_price" NUMERIC,
            "current_price" NUMERIC,
            "buy_now_price" NUMERIC NOT NULL,
            "auction_start" DATETIME,
            "auction_end" DATETIME,
            "status" TEXT NOT NULL CHECK("status" IN ('active', 'sold', 'cancelled', 'ended', 'draft')),
            "image_encoded" VARCHAR NOT NULL,
            "bids" INTEGER,
            "purchases" INTEGER NOT NULL,
            "average_review" NUMERIC,
            "total_reviews" INTEGER NOT NULL,
            "created_at" DATETIME NOT NULL,
            "updated_at" DATETIME NOT NULL,
            FOREIGN KEY("category_id") REFERENCES "categories"("category_id"),
            FOREIGN KEY("user_id") REFERENCES "users"("user_id")
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS order_items (
            "order_item_id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "order_id" INTEGER NOT NULL,
            "listing_id" INTEGER NOT NULL,
            "quantity" INTEGER NOT NULL,
            "price" NUMERIC NOT NULL,
            "total_price" NUMERIC NOT NULL,
            "created_at" DATETIME NOT NULL,
            "updated_at" DATETIME NOT NULL,
            FOREIGN KEY("listing_id") REFERENCES "listings"("listing_id"),
            FOREIGN KEY("order_id") REFERENCES "orders"("order_id")
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS orders (
            "order_id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "user_id" INTEGER NOT NULL,
            "order_date" DATETIME NOT NULL,
            "status" TEXT NOT NULL CHECK("status" IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled', 'returned')),
            "total_amount" NUMERIC NOT NULL,
            "payment_status" TEXT NOT NULL CHECK("payment_status" IN ('pending', 'completed', 'failed', 'refunded')),
            "payment_method" VARCHAR NOT NULL,
            "shipping_address" TEXT NOT NULL,
            "shipping_method" VARCHAR NOT NULL,
            "tracking_number" VARCHAR NOT NULL,
            "shipping_cost" NUMERIC NOT NULL,
            "created_at" DATETIME NOT NULL,
            "updated_at" DATETIME NOT NULL,
            FOREIGN KEY("user_id") REFERENCES "users"("user_id")
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS reviews (
            "review_id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "listing_id" INTEGER NOT NULL,
            "user_id" INTEGER NOT NULL,
            "username" VARCHAR NOT NULL,
            "title" VARCHAR NOT NULL,
            "description" TEXT NOT NULL,
            "stars" INTEGER NOT NULL,
            "created_at" DATETIME,
            FOREIGN KEY("listing_id") REFERENCES "listings"("listing_id"),
            FOREIGN KEY("user_id") REFERENCES "users"("user_id"),
            FOREIGN KEY("username") REFERENCES "users"("username")
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS sessions (
            "session_id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "user_id" INTEGER NOT NULL,
            "token" TEXT NOT NULL,
            "created_at" DATETIME NOT NULL,
            FOREIGN KEY("user_id") REFERENCES "users"("user_id")
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS staff_users (
            "staff_id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "name" VARCHAR NOT NULL,
            "email" VARCHAR NOT NULL,
            "phone" VARCHAR NOT NULL,
            "role" VARCHAR NOT NULL CHECK ("role" in ('staff', 'admin')),
            "password_hash" TEXT NOT NULL,
            "status" VARCHAR NOT NULL,
            "created_at" DATETIME NOT NULL,
            "updated_at" DATETIME NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS support_tickets (
            "ticket_id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "user_id" INTEGER NOT NULL,
            "order_id" INTEGER NOT NULL,
            "subject" VARCHAR NOT NULL,
            "status" VARCHAR NOT NULL,
            "priority" VARCHAR NOT NULL,
            "assigned_to" INTEGER NOT NULL,
            "created_at" DATETIME NOT NULL,
            "updated_at" DATETIME NOT NULL,
            FOREIGN KEY("assigned_to") REFERENCES "staff_users"("staff_id"),
            FOREIGN KEY("order_id") REFERENCES "orders"("order_id"),
            FOREIGN KEY("user_id") REFERENCES "users"("user_id")
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS ticket_messages (
            "message_id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "ticket_id" INTEGER NOT NULL,
            "user_sender_id" INTEGER,
            "staff_sender_id" INTEGER,
            "message" TEXT NOT NULL,
            "sent_at" DATETIME NOT NULL,
            FOREIGN KEY("staff_sender_id") REFERENCES "staff_users"("staff_id"),
            FOREIGN KEY("ticket_id") REFERENCES "support_tickets"("ticket_id"),
            FOREIGN KEY("user_sender_id") REFERENCES "users"("user_id")
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS transactions (
            "transaction_id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "listing_id" INTEGER NOT NULL,
            "buyer_id" INTEGER NOT NULL,
            "seller_id" INTEGER NOT NULL,
            "transaction_date" DATETIME NOT NULL,
            "transaction_type" TEXT NOT NULL CHECK("transaction_type" IN ('auction', 'buy_now')),
            "amount" NUMERIC NOT NULL,
            "payment_method" VARCHAR NOT NULL,
            status TEXT NOT NULL CHECK("status" IN ('pending', 'completed', 'failed', 'refunded')),
            "shipping_address" TEXT NOT NULL,
            "tracking_number" VARCHAR NOT NULL,
            "created_at" DATETIME NOT NULL,
            "updated_at" DATETIME NOT NULL,
            FOREIGN KEY("buyer_id") REFERENCES "users"("user_id"),
            FOREIGN KEY("listing_id") REFERENCES "listings"("listing_id"),
            FOREIGN KEY("seller_id") REFERENCES "users"("user_id")
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS profiles (
            "profile_id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "user_id" INTEGER NOT NULL UNIQUE,
            "first_name" VARCHAR NOT NULL,
            "last_name" VARCHAR,
            "date_of_birth" DATE,
            "phone_number" VARCHAR(10) NOT NULL UNIQUE,
            "address" TEXT NOT NULL,
            "city" VARCHAR NOT NULL,
            "state" VARCHAR NOT NULL,
            "country" VARCHAR NOT NULL,
            "profile_picture" VARCHAR,
            "bio" TEXT,
            "social_links" JSON,
            "created_at" DATETIME NOT NULL,
            "updated_at" DATETIME NOT NULL,
            FOREIGN KEY("user_id") REFERENCES "users"("user_id")
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS users (
            "user_id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "username" VARCHAR NOT NULL UNIQUE,
            "password_hash" TEXT NOT NULL,
            "email" VARCHAR NOT NULL,
            "created_at" DATETIME NOT NULL,
            "updated_at" DATETIME NOT NULL,
            "last_login" DATETIME NOT NULL,
            "is_active" BOOLEAN NOT NULL DEFAULT 1
        );
        """
    ]

    for table in tables:
        cursor.execute(table)

    db.commit()
