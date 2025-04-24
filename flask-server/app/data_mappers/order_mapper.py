from pymysql import cursors
from datetime import datetime

from ..database import get_db
from ..entities import Order, OrderItem


class OrderMapper:
    @staticmethod
    def get_all_orders(user_id: int, db_session=None):
        """
        Retrieve all orders from the database.

        Args:
            user_id (int): The unique identifier of the user.
            db_session: Optional database session to be used in tests.

        Returns:
            list: A list of order dictionaries.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM orders WHERE user_id = %s", (user_id,))
        orders = cursor.fetchall()
        return [Order(**order).to_dict() for order in orders]


    @staticmethod
    def get_order_by_id(order_id: int, db_session=None):
        """
        Retrieve an order by its ID.

        Args:
            order_id (int): The ID of the order to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            dict: Order details if found, otherwise None.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
        order = cursor.fetchone()
        return Order(**order).to_dict() if order else None


    @staticmethod
    def create_order(data: dict, db_session=None):
        """
        Create a new order in the database.

        Args:
            data (dict): Dictionary containing order details.
            db_session: Optional database session to be used in tests.

        Returns:
            int: The ID of the newly created order.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        statement = """
            INSERT INTO orders 
            (user_id, order_date, status, created_at, updated_at) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(statement, tuple(Order(**data).to_dict().values())[1:]) # Exclude order_id (auto-incremented)
        db.commit()
        return cursor.lastrowid


    @staticmethod
    def create_order_item(data: dict, db_session=None):
        """
        Create a new order item in the database.

        Args:
            data (dict): Dictionary containing order item details.
            db_session: Optional database session to be used in tests.

        Returns:
            int: The ID of the newly created order item.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        statement = """
            INSERT INTO order_items 
            (order_id, listing_id, quantity, price, total_price, created_at, updated_at) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(statement, tuple(OrderItem(**data).to_dict().values())[1:]) # Exclude order_item_id (auto-incremented)
        db.commit()
        return cursor.lastrowid


    @staticmethod
    def update_order(order_id: int, data: dict, db_session=None):
        """
        Update an existing order.

        Args:
            order_id (int): The ID of the order to update.
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
        conditions = [f"{key} = %s" for key in data if key not in ["order_id", "created_at", "updated_at"]]
        values = [data.get(key) for key in data if key not in ["order_id", "created_at", "updated_at"]]
        values.append(datetime.now())
        values.append(order_id)
        statement = f"UPDATE orders SET {', '.join(conditions)}, updated_at = %s WHERE order_id = %s"
        cursor.execute(statement, values)
        db.commit()
        return cursor.rowcount


    @staticmethod
    def delete_order(order_id: int, db_session=None):
        """
        Delete an order by its ID.

        Args:
            order_id (int): The ID of the order to delete.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows deleted.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
        db.commit()
        return cursor.rowcount

