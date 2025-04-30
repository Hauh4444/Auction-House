from pymysql import cursors
from ..database.connection import get_db
from aftership import AfterShip


class DeliveryMapper:
    @staticmethod
    def get_all_deliveries(user_id, db_session=None):
        """
        Retrieve all deliveries for a specific user.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor)
        cursor.execute("SELECT * FROM deliveries WHERE user_id = %s", (user_id,))
        results = cursor.fetchall()
        cursor.close()
        return results

    @staticmethod
    def get_delivery_by_id(delivery_id, db_session=None):
        """
        Retrieve a specific delivery by its ID.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor)
        cursor.execute("SELECT * FROM deliveries WHERE delivery_id = %s", (delivery_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    @staticmethod
    def create_delivery(data, db_session=None):
        """
        Create a new delivery record in the database.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        query = """
            INSERT INTO deliveries (user_id, tracking_code, created_at, updated_at)
            VALUES (%s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """
        cursor.execute(query, (data["user_id"], data["tracking_code"]))
        db.commit()
        delivery_id = cursor.lastrowid
        cursor.close()
        return delivery_id

    @staticmethod
    def update_delivery(delivery_id, data, db_session=None):
        """
        Update an existing delivery.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor)
        set_clause = ", ".join([f"{key} = %s" for key in data])
        values = list(data.values()) + [delivery_id]
        query = f"UPDATE deliveries SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE delivery_id = %s"
        cursor.execute(query, values)
        db.commit()
        updated_rows = cursor.rowcount
        cursor.close()
        return updated_rows

    @staticmethod
    def delete_delivery(delivery_id, db_session=None):
        """
        Delete a delivery by its ID.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor)
        cursor.execute("DELETE FROM deliveries WHERE delivery_id = %s", (delivery_id,))
        db.commit()
        deleted_rows = cursor.rowcount
        cursor.close()
        return deleted_rows

    @staticmethod
    def track_delivery(tracking_code):
        """
        Track a delivery using AfterShip.

        Args:
            tracking_code (str): The tracking code of the shipment.

        Returns:
            dict: The AfterShip tracking details.
        """
        aftership = AfterShip(api_key=os.getenv("AFTERSHIP_API_KEY"))
        tracking = aftership.tracking.get(tracking_code)
        return tracking

    @staticmethod
    def get_delivery_reference(delivery_id, db_session=None):
        """
        Retrieve the reference data for a delivery by its ID.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor)
        cursor.execute("SELECT * FROM deliveries WHERE delivery_id = %s", (delivery_id,))
        result = cursor.fetchone()
        cursor.close()
        return result
