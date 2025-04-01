from pymysql import cursors

from ..database.connection import get_db
from ..entities import Delivery


class DeliveryMapper:
    @staticmethod
    def get_all_deliveries(user_id, db_session=None):
        """
        Retrieve all deliveries associated with a user.

        Args:
            user_id (int): The ID of the user whose deliveries are being retrieved.
            db_session (optional): A database session for testing or direct queries.

        Returns:
            list[dict]: A list of dictionaries representing the user's deliveries.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM deliveries WHERE user_id = %s", (user_id,))
        deliveries = cursor.fetchall()
        return [Delivery(**delivery).to_dict() for delivery in deliveries]

    @staticmethod
    def get_delivery_by_id(delivery_id, db_session=None):
        """
        Retrieve a delivery record by its ID.

        Args:
            delivery_id (int): The ID of the delivery to retrieve.
            db_session (optional): A database session for testing or direct queries.

        Returns:
            dict | None: A dictionary representing the delivery if found, otherwise None.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM deliveries WHERE delivery_id = %s", (delivery_id,))
        delivery = cursor.fetchone()
        return Delivery(**delivery).to_dict() if delivery else None

    @staticmethod
    def create_delivery(data, db_session=None):
        """
        Create a new delivery record in the database.

        Args:
            data (dict): A dictionary containing delivery details.
            db_session (optional): A database session for testing or direct queries.

        Returns:
            int: The ID of the newly created delivery.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        statement = """
            INSERT INTO deliveries 
            (order_item_id, user_id, address, city, state, country, delivery_status, 
            tracking_number, courier, estimated_delivery_date, delivered_at, created_at, updated_at) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(statement, tuple(Delivery(**data).to_dict().values())[1:])  # Exclude delivery_id (auto-incremented)
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def update_delivery(delivery_id, data, db_session=None):
        """
        Update an existing delivery record.

        Args:
            delivery_id (int): The ID of the delivery to update.
            data (dict): A dictionary containing the fields to update.
            db_session (optional): A database session for testing or direct queries.

        Returns:
            int: The number of rows updated (should be 1 if successful).
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        conditions = [f"{key} = %s" for key in data if key not in ["delivery_id", "created_at"]]
        values = [data.get(key) for key in data if key not in ["delivery_id", "created_at"]]
        values.append(delivery_id)
        statement = f"UPDATE deliveries SET {', '.join(conditions)}, updated_at = CURRENT_TIMESTAMP WHERE delivery_id = %s"
        cursor.execute(statement, values)
        db.commit()
        return cursor.rowcount

    @staticmethod
    def delete_delivery(delivery_id, db_session=None):
        """
        Delete a delivery record by its ID.

        Args:
            delivery_id (int): The ID of the delivery to delete.
            db_session (optional): A database session for testing or direct queries.

        Returns:
            int: The number of rows deleted (should be 1 if successful).
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("DELETE FROM deliveries WHERE delivery_id = %s", (delivery_id,))
        db.commit()
        return cursor.rowcount
