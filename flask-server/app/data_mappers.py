from .database import get_db
from .entities import Category, Listing

class ListingMapper:
    @staticmethod
    def get_all_listings(args):
        db = get_db()
        cursor = db.cursor()
        statement = "SELECT * FROM listings"
        conditions = [f"{key}='{args[key]}'" for key in ["category_id", "listing_type"] if key in args]
        if "min_price" in args:
            conditions.append(f"current_price > {args['min_price']}")
        if "max_price" in args:
            conditions.append(f"current_price < {args['max_price']}")
        if conditions:
            statement += " WHERE " + " AND ".join(conditions)
        if "sort" in args and "order" in args:
            statement += f" ORDER BY {args['sort']} {args['order'].upper()}"
        if "start" in args and "range" in args:
            statement += f" LIMIT {args['range']} OFFSET {args['start']}"
        cursor.execute(statement)
        listings = cursor.fetchall()
        return [Listing(*listing).to_dict() for listing in listings]

    @staticmethod
    def get_listing_by_id(listing_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM listings WHERE listing_id = ?", (listing_id,))
        listing = cursor.fetchone()
        return Listing(*listing).to_dict() if listing else None

    @staticmethod
    def create_listing(data):
        db = get_db()
        cursor = db.cursor()
        sql = ("""INSERT INTO listings 
                  (user_id, title, title_short, description, category, type, starting_price, reserve_price, 
                  current_price, auction_start, auction_end, status, image_encoded, purchases, average_review, 
                  total_reviews, created_at, updated_at) 
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))""")
        cursor.execute(sql, (data["name"], data["description"], data["image_encoded"]))
        db.commit()
        return cursor.lastrowid  # Return new listing ID

    @staticmethod
    def update_listing(listing_id, data):
        db = get_db()
        cursor = db.cursor()
        sql = """UPDATE listings 
                 SET user_id = ?, title = ?, title_short = ?, description = ?, category = ?, type = ?, starting_price = ?,
                 reserve_price = ?, current_price = ?, auction_start = ?, auction_end = ?, status = ?, image_encoded = ?, 
                 purchases = ?, average_review = ?, total_reviews = ?, updated_at = datetime('now') 
                 WHERE listing_id = ?"""
        cursor.execute(sql, (data, listing_id))
        db.commit()
        return cursor.rowcount  # Returns number of rows updated

    @staticmethod
    def delete_listing(listing_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM listings WHERE listing_id = ?", (listing_id,))
        db.commit()
        return cursor.rowcount  # Returns number of rows deleted

class CategoryMapper:
    @staticmethod
    def get_all_categories():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()
        return [Category(*category).to_dict() for category in categories]

    @staticmethod
    def get_category_by_id(category_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM categories WHERE category_id = ?", (category_id,))
        category = cursor.fetchone()
        return Category(*category).to_dict() if category else None

    @staticmethod
    def create_category(data):
        db = get_db()
        cursor = db.cursor()
        sql = ("""INSERT INTO categories 
                  (name, description, image_encoded, created_at, updated_at) 
                  VALUES (?, ?, ?, datetime('now'), datetime('now'))""")
        cursor.execute(sql, (data["name"], data["description"], data["image_encoded"]))
        db.commit()
        return cursor.lastrowid  # Return new category ID

    @staticmethod
    def update_category(category_id, data):
        db = get_db()
        cursor = db.cursor()
        sql = """UPDATE categories 
                 SET name = ?, description = ?, image_encoded = ?, updated_at = datetime('now') 
                 WHERE category_id = ?"""
        cursor.execute(sql, (data["name"], data["description"], data["image_encoded"], category_id))
        db.commit()
        return cursor.rowcount  # Returns number of rows updated

    @staticmethod
    def delete_category(category_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM categories WHERE category_id = ?", (category_id,))
        db.commit()
        return cursor.rowcount  # Returns number of rows deleted
