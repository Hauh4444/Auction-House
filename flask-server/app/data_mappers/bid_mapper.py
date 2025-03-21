from ..database.connection import get_db
from ..entities import Bid


class BidMapper:
    @staticmethod
    def get_all_bids(db_session=None):
        """
        Retrieve all bids from the database.

        Args:
            db_session: Optional database session to be used in tests.

        Returns:
            list: A list of bid dictionaries.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM bids")
        bids = cursor.fetchall()
        return [Bid(**bid).to_dict() for bid in bids]


    @staticmethod
    def get_bid_by_id(bid_id, db_session=None):
        """
        Retrieve a bid by its ID.

        Args:
            bid_id (int): The ID of the bid to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            dict: Bid details if found, otherwise None.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM bids WHERE bid_id = ?", (bid_id,))
        bid = cursor.fetchone()
        return Bid(**bid).to_dict() if bid else None

    
    @staticmethod
    def create_bid(data, db_session=None):
        """
        Create a new category in the database.

        Args:
            data (dict): Dictionary containing category details.
            db_session: Optional database session to be used in tests.

        Returns:
            int: The ID of the newly created category.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        statement = """
            INSERT INTO categories 
            (listing_id, user_id, amount, created_at) 
            VALUES (?, ?, ?, ?)
        """
        cursor.execute(statement, tuple(Bid(**data).to_dict().values())[1:])
        db.commit()
        return cursor.lastrowid
