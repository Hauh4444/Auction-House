from .database import get_db
from .entities import Category, Listing
from datetime import datetime

class ListingMapper:
    @staticmethod
    def get_all_listings(args):
        db = get_db()
        cursor = db.cursor()
        statement = "SELECT * FROM listings"
        # TODO write CONTAINS into statement to handle "query",
        #  SELECT where name contains "query" plus SELECT where description contains "query"
        # Set conditions for any value we might want to directly check against
        conditions = [f"{key}='{args[key]}'" for key in ["category_id", "listing_type"] if key in args]
        # Price conditions
        if "min_price" in args:
            conditions.append(f"buy_now_price > {args['min_price']}")
        if "max_price" in args:
            conditions.append(f"buy_now_price < {args['max_price']}")
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
        db = get_db()
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM listings WHERE listing_id={listing_id}")
        listing = cursor.fetchone()
        return Listing(**listing).to_dict() if listing else None

    @staticmethod
    def create_listing(data):
        db = get_db()
        cursor = db.cursor()
        statement = (
            """
                INSERT INTO listings 
                (listing_id, user_id, title, title_short, description, category_id, listing_type, starting_price, reserve_price,
                current_price, buy_now_price, auction_start, auction_end, status, image_encoded, bids, purchases, average_review, 
                total_reviews, created_at, updated_at) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        )
        cursor.execute(statement, tuple(Listing(**data).to_dict().values()))
        db.commit()
        return cursor.lastrowid  # Return new listing ID

    @staticmethod
    def update_listing(listing_id, data):
        db = get_db()
        cursor = db.cursor()
        # Set/override update datetime
        data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Set conditions for update statement
        conditions = [f"{key}='{data[key]}'" for key in data if key not in ["listing_id", "created_at"]]
        # Create statement
        statement = "UPDATE listings SET " + ", ".join(conditions) + f" WHERE listing_id={listing_id}"
        cursor.execute(statement)
        db.commit()
        return cursor.rowcount  # Returns number of rows updated

    @staticmethod
    def delete_listing(listing_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM listings WHERE listing_id={listing_id}")
        db.commit()
        return cursor.rowcount  # Returns number of rows deleted

class CategoryMapper:
    @staticmethod
    def get_all_categories():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()
        return [Category(**category).to_dict() for category in categories]

    @staticmethod
    def get_category_by_id(category_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM categories WHERE category_id={category_id}")
        category = cursor.fetchone()
        return Category(**category).to_dict() if category else None

    @staticmethod
    def create_category(data):
        db = get_db()
        cursor = db.cursor()
        statement = (
            """
                INSERT INTO categories 
                (category_id, name, description, image_encoded, created_at, updated_at) 
                VALUES (?, ?, ?, ?, ?, ?)
            """
        )
        cursor.execute(statement, tuple(Category(**data).to_dict().values()))
        db.commit()
        return cursor.lastrowid  # Return new category ID

    @staticmethod
    def update_category(category_id, data):
        db = get_db()
        cursor = db.cursor()
        # Set/override update datetime
        data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Set conditions for update statement
        conditions = [f"{key}='{data[key]}'" for key in data if key not in ["category_id", "created_at"]]
        # Create statement
        statement = "UPDATE categories SET " + ", ".join(conditions) + f" WHERE category_id={category_id}"
        cursor.execute(statement)
        db.commit()
        return cursor.rowcount  # Returns number of rows updated

    @staticmethod
    def delete_category(category_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM categories WHERE category_id={category_id}")
        db.commit()
        return cursor.rowcount  # Returns number of rows deleted
