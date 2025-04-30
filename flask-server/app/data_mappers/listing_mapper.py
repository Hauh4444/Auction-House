from pymysql import cursors
from datetime import datetime

from ..database import get_db
from ..entities import Listing


class ListingMapper:
    @staticmethod
    def get_all_listings(args: dict, db_session=None):
        """
        Retrieve all listings with optional filtering, sorting, and pagination.

        Args:
            args (dict): Dictionary of query parameters.
            db_session: Optional database session to be used in tests.

        Returns:
            list: A list of listing dictionaries matching the query conditions.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        statement = "SELECT * FROM listings"
        conditions = []
        values = []

        # Add conditions
        if "user_id" in args:
            conditions.append("user_id = %s")
            values.append(args.get("user_id"))
        if "category_id" in args:
            conditions.append("category_id = %s")
            values.append(args.get("category_id"))
        if "listing_type" in args:
            conditions.append("listing_type = %s")
            values.append(args.get("listing_type"))
        if "min_price" in args:
            conditions.append("buy_now_price > %s")
            values.append(args.get("min_price"))
        if "max_price" in args:
            conditions.append("buy_now_price < %s")
            values.append(args.get("max_price"))
        if "query" in args:
            query = args.get("query")
            conditions.append("(title LIKE %s OR description LIKE %s)")
            values.extend([f"%{query}%", f"%{query}%"])

        if conditions:
            statement += " WHERE " + " AND ".join(conditions)

        # Add sorting
        if "sort" in args and "order" in args:
            statement += f" ORDER BY {args['sort']} {args['order'].upper()}"

        # Add pagination
        if "start" in args and "range" in args:
            statement += " LIMIT %s OFFSET %s"
            values.extend([int(args.get("range")), int(args.get("start"))])

        cursor.execute(statement, values)
        listings = cursor.fetchall()
        return [Listing(**listing).to_dict() for listing in listings]


    @staticmethod
    def get_listing_by_id(listing_id: int, db_session=None):
        """
        Retrieve a single listing by its ID.

        Args:
            listing_id (int): The ID of the listing to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            dict: Listing details if found, otherwise None.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM listings WHERE listing_id = %s", (listing_id,))
        listing = cursor.fetchone()
        return Listing(**listing).to_dict() if listing else None


    @staticmethod
    def create_listing(data: dict, db_session=None):
        """
        Create a new listing in the database.

        Args:
            data (dict): Dictionary containing listing details.
            db_session: Optional database session to be used in tests.

        Returns:
            int: The ID of the newly created listing.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        statement = """
            INSERT INTO listings 
            (user_id, title, title_short, description, item_specifics, category_id, listing_type, starting_price, 
            reserve_price, current_price, buy_now_price, auction_start, auction_end, status, image_encoded, bids, purchases, 
            average_review, total_reviews, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(statement, tuple(Listing(**data).to_dict().values())[1:])
        db.commit()
        return cursor.lastrowid


    @staticmethod
    def update_listing(listing_id: int, data: dict, db_session=None):
        """
        Update an existing listing.

        Args:
            listing_id (int): The ID of the listing to update.
            data (dict): Dictionary of fields to update.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows updated.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor)  # type: ignore
        set_clause = []
        values = []
        for key, value in data.items():
            if key not in ["listing_id", "created_at", "updated_at"]:
                increment_value = 1 if key == "bids" else None
                set_clause.append(f"{key} = {key} + %s" if increment_value else f"{key} = %s")
                values.append(increment_value if increment_value else value)
        values.append(datetime.now())
        values.append(listing_id)
        statement = f"UPDATE listings SET {', '.join(set_clause)}, updated_at = %s WHERE listing_id = %s"
        cursor.execute(statement, values)
        db.commit()
        return cursor.rowcount


    @staticmethod
    def delete_listing(listing_id: int, db_session=None):
        """
        Delete a listing by its ID.

        Args:
            listing_id (int): The ID of the listing to delete.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows deleted.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("DELETE FROM listings WHERE listing_id = %s", (listing_id,))
        db.commit()
        return cursor.rowcount

