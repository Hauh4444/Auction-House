from ..database import get_db
from ..entities.transaction import Transaction

class TransactionMapper:
    """Handles database operations related to transactions."""

    @staticmethod
    def get_all_transactions():
        """Retrieve all transactions from the database.

        Returns:
            list: A list of transaction dictionaries.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM transactions")
        transactions = cursor.fetchall()
        return [Transaction(**transaction).to_dict() for transaction in transactions]

    @staticmethod
    def get_transaction_by_id(transaction_id):
        """Retrieve a transaction by its ID.

        Args:
            transaction_id (int): The ID of the transaction to retrieve.

        Returns:
            dict: Transaction details if found, otherwise None.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM transactions WHERE transaction_id = ?", (transaction_id,))
        transaction = cursor.fetchone()
        return Transaction(**transaction).to_dict() if transaction else None

    @staticmethod
    def create_transaction(data):
        """Create a new transaction in the database.

        Args:
            data (dict): Dictionary containing transaction details.

        Returns:
            int: The ID of the newly created transaction.
        """
        db = get_db()
        cursor = db.cursor()
        statement = """
            INSERT INTO transactions 
            (listing_id, buyer_id, seller_id, transaction_date, transaction_type, amount, 
            payment_method, status, shipping_address, tracking_number, created_at, updated_at) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(statement, tuple(Transaction(**data).to_dict().values())[1:])  # Exclude transaction_id (auto-incremented)
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def update_transaction(transaction_id, data):
        """Update an existing transaction.

        Args:
            transaction_id (int): The ID of the transaction to update.
            data (dict): Dictionary of fields to update.

        Returns:
            int: Number of rows updated.
        """
        db = get_db()
        cursor = db.cursor()
        conditions = [f"{key} = ?" for key in data if key not in ["transaction_id", "created_at"]]
        values = [data[key] for key in data if key not in ["transaction_id", "created_at"]]
        values.append(transaction_id)
        statement = f"UPDATE transactions SET {', '.join(conditions)}, updated_at = CURRENT_TIMESTAMP WHERE transaction_id = ?"
        cursor.execute(statement, values)
        db.commit()
        return cursor.rowcount

    @staticmethod
    def delete_transaction(transaction_id):
        """Delete a transaction by its ID.

        Args:
            transaction_id (int): The ID of the transaction to delete.

        Returns:
            int: Number of rows deleted.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM transactions WHERE transaction_id = ?", (transaction_id,))
        db.commit()
        return cursor.rowcount
