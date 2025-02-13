from datetime import datetime
from .database import get_db
from .entities import Category, Listing


class ListingMapper:
    """Handles database operations related to listings."""

    @staticmethod
    def get_all_listings(args):
        """Retrieve all listings with optional filtering, sorting, and pagination.

        Args:
            args (dict): Dictionary of query parameters (e.g., category_id, min_price, query).

        Returns:
            list: A list of listing dictionaries matching the query conditions.
        """
        db = get_db()
        cursor = db.cursor()
        statement = "SELECT * FROM listings"
        # Set conditions for any value we might want to directly check against
        conditions = [f"{key}='{args[key]}'" for key in ["category_id", "listing_type"] if key in args]
        # Price conditions
        if "min_price" in args:
            conditions.append(f"buy_now_price > {args['min_price']}")
        if "max_price" in args:
            conditions.append(f"buy_now_price < {args['max_price']}")
        # SearchNav query filter
        if "query" in args:
            query = args["query"]
            conditions.append(f"(title LIKE '%{query}%' OR description LIKE '%{query}%')")
        # Add check conditions to statement
        if conditions:
            statement += " WHERE " + " AND ".join(conditions)
        # Sort conditions
        if "sort" in args and "order" in args:
            statement += f" ORDER BY {args['sort']} {args['order'].upper()}"
        # Start and range of entries conditions
        if "start" in args and "range" in args:
            statement += f" LIMIT {args['range']} OFFSET {args['start']}"

        cursor.execute(statement)
        listings = cursor.fetchall()
        return [Listing(**listing).to_dict() for listing in listings]

    @staticmethod
    def get_listing_by_id(listing_id):
        """Retrieve a single listing by its ID.

        Args:
            listing_id (int): The ID of the listing to retrieve.

        Returns:
            dict: Listing details if found, otherwise None.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM listings WHERE listing_id={listing_id}")
        listing = cursor.fetchone()
        return Listing(**listing).to_dict() if listing else None

    @staticmethod
    def create_listing(data):
        """Create a new listing in the database.

        Args:
            data (dict): Dictionary containing listing details.

        Returns:
            int: The ID of the newly created listing.
        """
        db = get_db()
        cursor = db.cursor()
        statement = """
            INSERT INTO listings 
            (listing_id, user_id, title, title_short, description, item_specifics, category_id, listing_type, starting_price, 
            reserve_price, current_price, buy_now_price, auction_start, auction_end, status, image_encoded, bids, purchases, 
            average_review, total_reviews, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(statement, tuple(Listing(**data).to_dict().values()))
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def update_listing(listing_id, data):
        """Update an existing listing.

        Args:
            listing_id (int): The ID of the listing to update.
            data (dict): Dictionary of fields to update.

        Returns:
            int: Number of rows updated.
        """
        db = get_db()
        cursor = db.cursor()
        data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conditions = [f"{key}='{data[key]}'" for key in data if key not in ["listing_id", "created_at"]]
        statement = "UPDATE listings SET " + ", ".join(conditions) + f" WHERE listing_id={listing_id}"
        cursor.execute(statement)
        db.commit()
        return cursor.rowcount

    @staticmethod
    def delete_listing(listing_id):
        """Delete a listing by its ID.

        Args:
            listing_id (int): The ID of the listing to delete.

        Returns:
            int: Number of rows deleted.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM listings WHERE listing_id={listing_id}")
        db.commit()
        return cursor.rowcount


class CategoryMapper:
    """Handles database operations related to categories."""

    @staticmethod
    def get_all_categories():
        """Retrieve all categories from the database.

        Returns:
            list: A list of category dictionaries.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()
        return [Category(**category).to_dict() for category in categories]

    @staticmethod
    def get_category_by_id(category_id):
        """Retrieve a category by its ID.

        Args:
            category_id (int): The ID of the category to retrieve.

        Returns:
            dict: CategoryNav details if found, otherwise None.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM categories WHERE category_id={category_id}")
        category = cursor.fetchone()
        return Category(**category).to_dict() if category else None

    @staticmethod
    def create_category(data):
        """Create a new category in the database.

        Args:
            data (dict): Dictionary containing category details.

        Returns:
            int: The ID of the newly created category.
        """
        db = get_db()
        cursor = db.cursor()
        statement = """
            INSERT INTO categories 
            (category_id, name, description, image_encoded, created_at, updated_at) 
            VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(statement, tuple(Category(**data).to_dict().values()))
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def update_category(category_id, data):
        """Update an existing category.

        Args:
            category_id (int): The ID of the category to update.
            data (dict): Dictionary of fields to update.

        Returns:
            int: Number of rows updated.
        """
        db = get_db()
        cursor = db.cursor()
        data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conditions = [f"{key}='{data[key]}'" for key in data if key not in ["category_id", "created_at"]]
        statement = "UPDATE categories SET " + ", ".join(conditions) + f" WHERE category_id={category_id}"
        cursor.execute(statement)
        db.commit()
        return cursor.rowcount

    @staticmethod
    def delete_category(category_id):
        """Delete a category by its ID.

        Args:
            category_id (int): The ID of the category to delete.

        Returns:
            int: Number of rows deleted.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM categories WHERE category_id={category_id}")
        db.commit()
        return cursor.rowcount
