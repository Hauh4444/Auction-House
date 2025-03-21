from . import db

class BidMapper:
    
    @staticmethod
    def create_bid(data, db_session=None):
        """
        Create a new bid and save it to the database.
        """
        # Create a new Bid instance
        bid = Bid(user=data['user'], amount=data['amount'])
        
        # Save the bid to the database (using the provided db_session or default session)
        if db_session:
            db_session.add(bid)
            db_session.commit()
        else:
            db.session.add(bid)
            db.session.commit()
        
        return bid.id

    @staticmethod
    def get_bid_by_id(bid_id, db_session=None):
        """
        Retrieve a bid by its ID from the database.
        """
        if db_session:
            return db_session.query(Bid).filter_by(id=bid_id).first()
        else:
            return db.session.query(Bid).filter_by(id=bid_id).first()

    @staticmethod
    def get_all_bids(db_session=None):
        """
        Retrieve all bids from the database.
        """
        if db_session:
            return db_session.query(Bid).all()
        else:
            return db.session.query(Bid).all()

# Assuming you have a Bid model defined with SQLAlchemy
class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
