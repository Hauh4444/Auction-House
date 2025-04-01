from pymysql import cursors

from ..database.connection import get_db
from ..entities import List, ListItem


class ListMapper:
    @staticmethod
    def get_lists(user_id, db_session=None):
        """
        Retrieve all lists associated with a user.

        Args:
            user_id (int): The ID of the user whose lists are being retrieved.
            db_session (optional): A database session for testing or direct queries.

        Returns:
            list[dict]: A list of dictionaries representing the user's lists.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM lists WHERE user_id = %s", (user_id,))
        lists = cursor.fetchall()
        return [List(**list_row).to_dict() for list_row in lists]

    @staticmethod
    def get_list_items(list_id, db_session=None):
        """
        Retrieve all items in a specific list.

        Args:
            list_id (int): The ID of the list whose items are being retrieved.
            db_session (optional): A database session for testing or direct queries.

        Returns:
            list[dict]: A list of dictionaries representing the list's items.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM list_items WHERE list_id = %s", (list_id,))
        list_items = cursor.fetchall()
        return [ListItem(**list_item).to_dict() for list_item in list_items]

    @staticmethod
    def get_list_by_id(list_id, db_session=None):
        """
        Retrieve a specific list by its ID.

        Args:
            list_id (int): The ID of the list to retrieve.
            db_session (optional): A database session for testing or direct queries.

        Returns:
            dict | None: A dictionary representing the list if found, otherwise None.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM lists WHERE list_id = %s", (list_id,))
        list_row = cursor.fetchone()
        return List(**list_row).to_dict() if list_row else None

    @staticmethod
    def create_list(data, db_session=None):
        """
        Create a new list record in the database.

        Args:
            data (dict): A dictionary containing list details.
            db_session (optional): A database session for testing or direct queries.

        Returns:
            int: The ID of the newly created list.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        statement = """
            INSERT INTO lists 
            (user_id, title, created_at) 
            VALUES (%s, %s, %s)
        """
        cursor.execute(statement, tuple(List(**data).to_dict().values())[1:])  # Exclude list_id (auto-incremented)
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def create_list_item(list_id, listing_id, db_session=None):
        """
        Create a new list item record in the database.

        Args:
            list_id (int): The ID of the list to which the item belongs.
            listing_id (int): The ID of the item being added to the list.
            db_session (optional): A database session for testing or direct queries.

        Returns:
            int: The ID of the newly created list item.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        statement = """
            INSERT INTO list_items 
            (list_id, listing_id, created_at) 
            VALUES (%s, %s, %s)
        """
        data = {"list_id": list_id, "listing_id": listing_id}
        cursor.execute(statement, tuple(ListItem(**data).to_dict().values())[1:])  # Exclude list_id (auto-incremented)
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def update_list(list_id, title, db_session=None):
        """
        Update the title of an existing list.

        Args:
            list_id (int): The ID of the list to update.
            title (str): The new title for the list.
            db_session (optional): A database session for testing or direct queries.

        Returns:
            int: The number of rows updated (should be 1 if successful).
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        statement = "UPDATE lists SET title = %s, updated_at = CURRENT_TIMESTAMP WHERE list_id = %s"
        cursor.execute(statement, (title, list_id))
        db.commit()
        return cursor.rowcount

    @staticmethod
    def delete_list(list_id, db_session=None):
        """
        Delete a list by its ID.

        Args:
            list_id (int): The ID of the list to delete.
            db_session (optional): A database session for testing or direct queries.

        Returns:
            int: The number of rows deleted (should be 1 if successful).
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("DELETE FROM lists WHERE list_id = %s", (list_id,))
        db.commit()
        return cursor.rowcount

    @staticmethod
    def delete_list_item(list_id, listing_id, db_session=None):
        """
        Delete a specific list item by its list ID and listing ID.

        Args:
            list_id (int): The ID of the list containing the item.
            listing_id (int): The ID of the item to be removed from the list.
            db_session (optional): A database session for testing or direct queries.

        Returns:
            int: The number of rows deleted (should be 1 if successful).
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("DELETE FROM list_items WHERE list_id = %s AND listing_id = %s", (list_id, listing_id))
        db.commit()
        return cursor.rowcount
