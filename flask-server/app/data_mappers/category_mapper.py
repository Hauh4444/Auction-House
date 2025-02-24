from ..database import get_db
from ..entities.category import Category


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
            dict: Category details if found, otherwise None.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM categories WHERE category_id=?", (category_id,))
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
        set_clause = ", ".join([f"{key}=?" for key in data if key not in ["category_id", "created_at"]])
        values = [data[key] for key in data if key not in ["category_id", "created_at"]]
        values.append(category_id)
        statement = f"UPDATE categories SET {set_clause} WHERE category_id=?"
        cursor.execute(statement, values)
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
        cursor.execute("DELETE FROM categories WHERE category_id=?", (category_id,))
        db.commit()
        return cursor.rowcount
