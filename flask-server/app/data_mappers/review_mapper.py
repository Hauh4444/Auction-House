from pymysql import cursors
from datetime import datetime

from ..database import get_db
from ..entities import Review


class ReviewMapper:
    @staticmethod
    def get_all_reviews(args: dict, db_session=None):
        """
        Retrieve all reviews with optional filtering

        Args:
            args (dict): Dictionary of query parameters.
            db_session: Optional database session to be used in tests.

        Returns:
            list: A list of review dictionaries matching the query conditions.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        statement = "SELECT * FROM reviews"
        values = []

        # Add conditions
        if "listing_id" in args:
            statement += " WHERE listing_id = %s"
            values.append(args.get("listing_id"))
        if "user_id" in args:
            statement += " WHERE user_id = %s"
            values.append(args.get("user_id"))

        # Add sorting
        if "sort" in args and "order" in args:
            statement += f" ORDER BY {args['sort']} {args['order'].upper()}"

        # Add start and range
        if "start" in args and "range" in args:
            statement += " LIMIT %s OFFSET %s"
            values.extend([int(args.get("range")), int(args.get("start"))])

        cursor.execute(statement, values)
        reviews = cursor.fetchall()
        return [Review(**review).to_dict() for review in reviews]


    @staticmethod
    def get_review_by_id(review_id: int, db_session=None):
        """
        Retrieve a review by its ID.

        Args:
            review_id (int): The ID of the review to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            dict: Review details if found, otherwise None.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM reviews WHERE review_id = %s", (review_id,))
        review = cursor.fetchone()
        return Review(**review).to_dict() if review else None


    @staticmethod
    def create_review(data: dict, db_session=None):
        """
        Create a new review in the database.

        Args:
            data (dict): Dictionary containing review details.
            db_session: Optional database session to be used in tests.

        Returns:
            int: The ID of the newly created review.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        statement = """
            INSERT INTO reviews 
            (listing_id, user_id, username, title, description, stars, created_at) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        # Explicitly extract the values from the data dictionary, excluding review_id if it exists
        values = [
            data.get("listing_id"),
            data.get("user_id"),
            data.get("username"),
            data.get("title"),
            data.get("description"),
            data.get("stars"),
            data.get("created_at")
        ]
        cursor.execute(statement, values)
        db.commit()
        return cursor.lastrowid


    @staticmethod
    def update_review(review_id: int, data: dict, db_session=None):
        """
        Update an existing review.

        Args:
            review_id (int): The ID of the review to update.
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
        set_clause = ", ".join([f"{key} = %s" for key in data if key not in ["review_id", "updated_at"]])
        values = [data.get(key) for key in data if key not in ["review_id", "updated_at"]]
        values.append(datetime.now())
        values.append(review_id)
        statement = f"UPDATE reviews SET {set_clause}, updated_at = %s WHERE review_id = %s"
        cursor.execute(statement, values)
        db.commit()
        return cursor.rowcount


    @staticmethod
    def delete_review(review_id: int, db_session=None):
        """
        Delete a review by its ID.

        Args:
            review_id (int): The ID of the review to delete.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows deleted.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("DELETE FROM reviews WHERE review_id = %s", (review_id,))
        db.commit()
        return cursor.rowcount
