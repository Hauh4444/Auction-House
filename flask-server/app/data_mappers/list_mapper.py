from ..database import get_db
from ..entities import List, ListItem


class ListMapper:
    """Handles database operations related to lists."""
    @staticmethod
    def get_lists(user_id, db_session=None):
        """
        Retrieve all user's lists from the database.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM lists WHERE user_id = ?", (user_id,))
        lists = cursor.fetchall()
        return [List(**list).to_dict() for list in lists]


    @staticmethod
    def get_list_items(list_id, db_session=None):
        """
        Retrieve all items in a user's list from the database
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM list_items WHERE list_id = ?", (list_id,))
        list_items = cursor.fetchall()
        return [ListItem(**list_item).to_dict() for list_item in list_items]


    @staticmethod
    def get_list_by_id(list_id, db_session=None):
        """
        Retrieve a list by its ID.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM lists WHERE list_id = ?", (list_id,))
        list = cursor.fetchone()
        return List(**list).to_dict() if list else None


    @staticmethod
    def create_list(data, db_session=None):
        """
        Create a new list record in the database.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        statement = """
            INSERT INTO lists 
            (user_id, title, created_at) 
            VALUES (?, ?, ?)
        """
        cursor.execute(statement, tuple(List(**data).to_dict().values())[1:]) # Exclude list_id (auto-incremented)
        db.commit()
        return cursor.lastrowid


    @staticmethod
    def create_list_item(list_id, listing_id, db_session=None):
        """
        Create a new list item record in the database
        """
        db = db_session or get_db()
        cursor = db.cursor()
        statement = """
            INSERT INTO list_items 
            (list_id, listing_id, created_at) 
            VALUES (?, ?, ?)
        """
        data = {"list_id": list_id, "listing_id": listing_id}
        cursor.execute(statement, tuple(ListItem(**data).to_dict().values())[1:])  # Exclude list_id (auto-incremented)
        db.commit()
        return cursor.lastrowid


    @staticmethod
    def update_list(list_id, title, db_session=None):
        """
        Update an existing list.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        statement = f"UPDATE lists SET title = ?, updated_at = CURRENT_TIMESTAMP WHERE list_id = ?"
        cursor.execute(statement, (title, list_id))
        db.commit()
        return cursor.rowcount


    @staticmethod
    def delete_list(list_id, db_session=None):
        """
        Delete a list by its ID.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM lists WHERE list_id = ?", (list_id,))
        db.commit()
        return cursor.rowcount


    @staticmethod
    def delete_list_item(list_id, listing_id, db_session=None):
        """
        Delete a list item by its list ID and listing ID
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM list_items WHERE list_id = ? AND listing_id = ?", (list_id, listing_id))
        db.commit()
        return cursor.rowcount
