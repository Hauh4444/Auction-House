from pymysql import cursors

from ..database import get_db
from ..entities import Category
from datetime import datetime

class CategoryMapper:
    @staticmethod
    def get_all_categories(db_session=None):
        """
        Retrieve all categories from the database.

        Args:
            db_session: Optional database session to be used in tests.

        Returns:
            list: A list of category dictionaries.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()
        return [Category(**category).to_dict() for category in categories]


    @staticmethod
    def get_category_by_id(category_id: int, db_session=None):
        """
        Retrieve a category by its ID.

        Args:
            category_id (int): The ID of the category to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            dict: Category details if found, otherwise None.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM categories WHERE category_id = %s", (category_id,))
        category = cursor.fetchone()
        return Category(**category).to_dict() if category else None


    @staticmethod
    def create_category(data: dict, db_session=None):
        """
        Create a new category in the database.

        Args:
            data (dict): Dictionary containing category details.
            db_session: Optional database session to be used in tests.

        Returns:
            int: The ID of the newly created category.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        statement = """
            INSERT INTO categories 
            (name, description, image_encoded, created_at, updated_at) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(statement, tuple(Category(**data).to_dict().values())[1:])
        db.commit()
        return cursor.lastrowid


    @staticmethod
    def update_category(category_id: int, data: dict, db_session=None):
        """
        Update an existing category.

        Args:
            category_id (int): The ID of the category to update.
            data (dict): Dictionary of fields to update.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows updated.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        for key, value in data.items():
            if isinstance(value, str):
                try:
                    data[key] = datetime.strptime(value, '%a, %d %b %Y %H:%M:%S GMT')
                except ValueError:
                    pass
            if isinstance(value, datetime):
                data[key] = value.strftime('%Y-%m-%d %H:%M:%S')
        set_clause = ", ".join([f"{key} = %s" for key in data if key not in ["category_id", "created_at"]])
        values = [data.get(key) for key in data if key not in ["category_id", "created_at"]]
        values.append(category_id)
        statement = f"UPDATE categories SET {set_clause} WHERE category_id = %s"
        cursor.execute(statement, values)
        db.commit()
        return cursor.rowcount


    @staticmethod
    def delete_category(category_id: int, db_session=None):
        """
        Delete a category by its ID.

        Args:
            category_id (int): The ID of the category to delete.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows deleted.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("DELETE FROM categories WHERE category_id = %s", (category_id,))
        db.commit()
        return cursor.rowcount
