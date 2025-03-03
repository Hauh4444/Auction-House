from ..database import get_db
from ..entities import Delivery


class DeliveryMapper:
    """Handles database operations related to deliveries."""
    @staticmethod
    def get_all_deliveries(db_session=None):
        """Retrieve all deliveries from the database.

        Args:
            db_session: Optional database session to be used in tests.

        Returns:
            list: A list of delivery dictionaries.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM deliveries")
        deliveries = cursor.fetchall()
        return [Delivery(**delivery).to_dict() for delivery in deliveries]


    @staticmethod
    def get_delivery_by_id(delivery_id, db_session=None):
        """Retrieve a delivery by its ID.

        Args:
            delivery_id (int): The ID of the delivery to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            dict: Delivery details if found, otherwise None.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM deliveries WHERE delivery_id = ?", (delivery_id,))
        delivery = cursor.fetchone()
        return Delivery(**delivery).to_dict() if delivery else None


    @staticmethod
    def create_delivery(data, db_session=None):
        """Create a new delivery record in the database.

        Args:
            data (dict): Dictionary containing delivery details.
            db_session: Optional database session to be used in tests.

        Returns:
            int: The ID of the newly created delivery.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        statement = """
            INSERT INTO deliveries 
            (order_id, user_id, address, city, state, postal_code, country, delivery_status, 
            tracking_number, courier, estimated_delivery_date, delivered_at, created_at, updated_at) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(statement, tuple(Delivery(**data).to_dict().values())[1:]) # Exclude delivery_id (auto-incremented)
        db.commit()
        return cursor.lastrowid


    @staticmethod
    def update_delivery(delivery_id, data, db_session=None):
        """Update an existing delivery.

        Args:
            delivery_id (int): The ID of the delivery to update.
            data (dict): Dictionary of fields to update.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows updated.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        conditions = [f"{key} = ?" for key in data if key not in ["delivery_id", "created_at"]]
        values = [data[key] for key in data if key not in ["delivery_id", "created_at"]]
        values.append(delivery_id)
        statement = f"UPDATE deliveries SET {', '.join(conditions)}, updated_at = CURRENT_TIMESTAMP WHERE delivery_id = ?"
        cursor.execute(statement, values)
        db.commit()
        return cursor.rowcount


    @staticmethod
    def delete_delivery(delivery_id, db_session=None):
        """Delete a delivery by its ID.

        Args:
            delivery_id (int): The ID of the delivery to delete.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows deleted.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM deliveries WHERE delivery_id = ?", (delivery_id,))
        db.commit()
        return cursor.rowcount
