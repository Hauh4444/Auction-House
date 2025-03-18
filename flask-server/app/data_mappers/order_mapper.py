from ..database import get_db
from ..entities import Order, OrderItem


class OrderMapper:
    """Handles database operations related to orders."""
    @staticmethod
    def get_all_orders(user_id, db_session=None):
        """
        Retrieve all orders from the database.

        Args:
            user_id (int): The unique identifier of the user.
            db_session: Optional database session to be used in tests.

        Returns:
            list: A list of order dictionaries.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM orders WHERE user_id = ?", (user_id,))
        orders = cursor.fetchall()
        return [Order(**order).to_dict() for order in orders]


    @staticmethod
    def get_order_by_id(order_id, db_session=None):
        """
        Retrieve an order by its ID.

        Args:
            order_id (int): The ID of the order to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            dict: Order details if found, otherwise None.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
        order = cursor.fetchone()
        return Order(**order).to_dict() if order else None


    @staticmethod
    def create_order(data, db_session=None):
        """Create a new order in the database.

        Args:
            data (dict): Dictionary containing order details.
            db_session: Optional database session to be used in tests.

        Returns:
            int: The ID of the newly created order.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        statement = """
            INSERT INTO orders 
            (user_id, order_date, status, created_at, updated_at) 
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(statement, tuple(Order(**data).to_dict().values())[1:]) # Exclude order_id (auto-incremented)
        db.commit()
        return cursor.lastrowid


    @staticmethod
    def create_order_item(data, db_session=None):
        """Create a new order item in the database.

        Args:
            data (dict): Dictionary containing order item details.
            db_session: Optional database session to be used in tests.

        Returns:
            int: The ID of the newly created order item.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        statement = """
            INSERT INTO order_items 
            (order_id, listing_id, quantity, price, total_price, created_at, updated_at) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(statement, tuple(OrderItem(**data).to_dict().values())[1:]) # Exclude order_item_id (auto-incremented)
        db.commit()
        return cursor.lastrowid


    @staticmethod
    def update_order(order_id, data, db_session=None):
        """Update an existing order.

        Args:
            order_id (int): The ID of the order to update.
            data (dict): Dictionary of fields to update.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows updated.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        conditions = [f"{key} = ?" for key in data if key not in ["order_id", "created_at"]]
        values = [data.get(key) for key in data if key not in ["order_id", "created_at"]]
        values.append(order_id)
        statement = f"UPDATE orders SET {', '.join(conditions)}, updated_at = CURRENT_TIMESTAMP WHERE order_id = ?"
        cursor.execute(statement, values)
        db.commit()
        return cursor.rowcount


    @staticmethod
    def delete_order(order_id, db_session=None):
        """Delete an order by its ID.

        Args:
            order_id (int): The ID of the order to delete.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows deleted.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
        db.commit()
        return cursor.rowcount

