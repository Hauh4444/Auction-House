from ..database import get_db
from ..entities import Transaction


class TransactionMapper:
    """Handles database operations related to transactions."""
    @staticmethod
    def get_all_transactions(user_id, db_session=None):
        """
        Retrieve all transactions from the database.

        Args:
            user_id: Id of the user to retrieve transactions of
            db_session: Optional database session to be used in tests.

        Returns:
            list: A list of transaction dictionaries.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM transactions WHERE user_id = ?", (user_id,))
        transactions = cursor.fetchall()
        return [Transaction(**transaction).to_dict() for transaction in transactions]


    @staticmethod
    def get_transaction_by_id(transaction_id, db_session=None):
        """
        Retrieve a transaction by its ID.

        Args:
            transaction_id (int): The ID of the transaction to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            dict: Transaction details if found, otherwise None.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM transactions WHERE transaction_id = ?", (transaction_id,))
        transaction = cursor.fetchone()
        return Transaction(**transaction).to_dict() if transaction else None


    @staticmethod
    def create_transaction(data, db_session=None):
        """Create a new transaction in the database.

        Args:
            data (dict): Dictionary containing transaction details.
            db_session: Optional database session to be used in tests.

        Returns:
            int: The ID of the newly created transaction.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        statement = """
            INSERT INTO transactions 
            (order_id, user_id, transaction_date, transaction_type, amount, 
            shipping_cost, payment_method, payment_status, created_at, updated_at) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(statement, tuple(Transaction(**data).to_dict().values())[1:]) # Exclude transaction_id (auto-incremented)
        db.commit()
        return cursor.lastrowid


    @staticmethod
    def update_transaction(transaction_id, data, db_session=None):
        """Update an existing transaction.

        Args:
            transaction_id (int): The ID of the transaction to update.
            data (dict): Dictionary of fields to update.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows updated.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        conditions = [f"{key} = ?" for key in data if key not in ["transaction_id", "created_at"]]
        values = [data.get(key) for key in data if key not in ["transaction_id", "created_at"]]
        values.append(transaction_id)
        statement = f"UPDATE transactions SET {', '.join(conditions)}, updated_at = CURRENT_TIMESTAMP WHERE transaction_id = ?"
        cursor.execute(statement, values)
        db.commit()
        return cursor.rowcount


    @staticmethod
    def delete_transaction(transaction_id, db_session=None):
        """Delete a transaction by its ID.

        Args:
            transaction_id (int): The ID of the transaction to delete.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows deleted.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM transactions WHERE transaction_id = ?", (transaction_id,))
        db.commit()
        return cursor.rowcount
