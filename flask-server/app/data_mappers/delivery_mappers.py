from ..database import get_db
from ..entities.delivery import Delivery

class DeliveryMapper:
    """Handles database operations related to deliveries."""

    @staticmethod
    def get_all_deliveries():
        """Retrieve all deliveries from the database.

        Returns:
            list: A list of delivery dictionaries.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM deliveries")
        deliveries = cursor.fetchall()
        return [Delivery(**delivery).to_dict() for delivery in deliveries]

    @staticmethod
    def get_delivery_by_id(delivery_id):
        """Retrieve a delivery by its ID.

        Args:
            delivery_id (int): The ID of the delivery to retrieve.

        Returns:
            dict: Delivery details if found, otherwise None.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM deliveries WHERE delivery_id = ?", (delivery_id,))
        delivery = cursor.fetchone()
        return Delivery(**delivery).to_dict() if delivery else None

    @staticmethod
    def create_delivery(data):
        """Create a new delivery record in the database.

        Args:
            data (dict): Dictionary containing delivery details.

        Returns:
            int: The ID of the newly created delivery.
        """
        db = get_db()
        cursor = db.cursor()
        statement = """
            INSERT INTO deliveries 
            (order_id, user_id, address, city, state, postal_code, country, delivery_status, 
            tracking_number, courier, estimated_delivery_date, delivered_at, created_at, updated_at) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(statement, tuple(Delivery(**data).to_dict().values())[1:])  # Exclude delivery_id (auto-incremented)
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def update_delivery(delivery_id, data):
        """Update an existing delivery.

        Args:
            delivery_id (int): The ID of the delivery to update.
            data (dict): Dictionary of fields to update.

        Returns:
            int: Number of rows updated.
        """
        db = get_db()
        cursor = db.cursor()
        conditions = [f"{key} = ?" for key in data if key not in ["delivery_id", "created_at"]]
        values = [data[key] for key in data if key not in ["delivery_id", "created_at"]]
        values.append(delivery_id)
        statement = f"UPDATE deliveries SET {', '.join(conditions)}, updated_at = CURRENT_TIMESTAMP WHERE delivery_id = ?"
        cursor.execute(statement, values)
        db.commit()
        return cursor.rowcount

    @staticmethod
    def delete_delivery(delivery_id):
        """Delete a delivery by its ID.

        Args:
            delivery_id (int): The ID of the delivery to delete.

        Returns:
            int: Number of rows deleted.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM deliveries WHERE delivery_id = ?", (delivery_id,))
        db.commit()
        return cursor.rowcount
