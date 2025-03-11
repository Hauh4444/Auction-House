from ..database import get_db
from ..entities import List, ListItem


class ListMapper:
    """Handles database operations related to lists."""
    @staticmethod
    def get_all_list_items(list_id, db_session=None):
        """
        Retrieve all items in a list from the database

        Args:
            list_id (int): The ID of the list whos items to retrieve
            db_session: Optional database session to be used in tests

        Returns
            list: A list of list item dictionaries
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM list_items WHERE list_id = ?", (list_id,))
        list_items = cursor.fetchall()
        return [ListItem(**list_item).to_dict() for list_item in list_items]


    @staticmethod
    def get_all_lists(user_id, db_session=None):
        """
        Retrieve all lists from the database.

        Args:
            user_id (int): The ID of the user to retrieve lists of.
            db_session: Optional database session to be used in tests.

        Returns:
            list: A list of list dictionaries.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM lists WHERE user_id = ?", (user_id,))
        lists = cursor.fetchall()
        return [List(**list).to_dict() for list in lists]


    @staticmethod
    def get_list_by_id(list_id, db_session=None):
        """
        Retrieve a list by its ID.

        Args:
            list_id (int): The ID of the list to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            dict: List details if found, otherwise None.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM lists WHERE list_id = ?", (list_id,))
        list = cursor.fetchone()
        return List(**list).to_dict() if list else None


    @staticmethod
    def create_list(data, db_session=None):
        """Create a new list record in the database.

        Args:
            data (dict): Dictionary containing list details.
            db_session: Optional database session to be used in tests.

        Returns:
            int: The ID of the newly created list.
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
    def update_list(list_id, data, db_session=None):
        """Update an existing list.

        Args:
            list_id (int): The ID of the list to update.
            data (dict): Dictionary of fields to update.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows updated.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        conditions = [f"{key} = ?" for key in data if key == "title"]
        values = [data[key] for key in data if key == "title"]
        values.append(list_id)
        statement = f"UPDATE lists SET {', '.join(conditions)}, updated_at = CURRENT_TIMESTAMP WHERE list_id = ?"
        cursor.execute(statement, values)
        db.commit()
        return cursor.rowcount


    @staticmethod
    def delete_list(list_id, db_session=None):
        """Delete a list by its ID.

        Args:
            list_id (int): The ID of the list to delete.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows deleted.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM lists WHERE list_id = ?", (list_id,))
        db.commit()
        return cursor.rowcount
