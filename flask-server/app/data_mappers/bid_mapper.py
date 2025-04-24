from pymysql import cursors

from ..database import get_db
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
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM bids")
        bids = cursor.fetchall()
        return [Bid(**bid).to_dict() for bid in bids]


    @staticmethod
    def get_bid_by_id(bid_id: int, db_session=None):
        """
        Retrieve a bid by its ID.

        Args:
            bid_id (int): The ID of the bid to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            dict: Bid details if found, otherwise None.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM bids WHERE bid_id = %s", (bid_id,))
        bid = cursor.fetchone()
        return Bid(**bid).to_dict() if bid else None

    
    @staticmethod
    def create_bid(data: dict, db_session=None):
        """
        Create a new category in the database.

        Args:
            data (dict): Dictionary containing category details.
            db_session: Optional database session to be used in tests.

        Returns:
            int: The ID of the newly created category.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        statement = """
            INSERT INTO bids 
            (listing_id, user_id, amount, created_at) 
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(statement, tuple(Bid(**data).to_dict().values())[1:])
        db.commit()
        return cursor.lastrowid
