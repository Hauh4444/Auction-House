from flask_socketio import emit
from flask import jsonify, Response
from .data_mappers import BidMapper  # Assuming this mapper will interact with the DB
from . import socketio  # Import socketio from the app context

class BidService:
    @staticmethod
    def post_bid(data, db_session=None):
        """
        Posts a new bid and broadcasts it in real-time.

        Args:
            data: A dictionary containing the bid details.
            db_session: Optional database session for tests.

        Returns:
            A Response object with the success message and newly created bid, or an error message if validation fails.
        """
        if not data.get("user") or not data.get("amount"):
            data = {"error": "User and amount are required"}
            return Response(response=jsonify(data).get_data(), status=400, mimetype='application/json')

        # Save the bid using a data mapper (which interacts with the DB)
        bid_id = BidMapper.create_bid(data=data, db_session=db_session)

        # Broadcast the new bid in real-time
        socketio.emit('new_bid', data)  # Emit event to all connected clients

        data = {"message": "Bid posted", "bid_id": bid_id, "bid": data}
        return Response(response=jsonify(data).get_data(), status=201, mimetype='application/json')

    @staticmethod
    def get_bid_by_id(bid_id, db_session=None):
        """
        Retrieves a specific bid by its ID.

        Args:
            bid_id: The ID of the bid to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object with the bid data if found, otherwise a 404 error with a message.
        """
        bid = BidMapper.get_bid_by_id(bid_id=bid_id, db_session=db_session)

        if bid:
            data = {"message": "Bid found", "bid": bid}
            return Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')

        data = {"error": "Bid not found"}
        return Response(response=jsonify(data).get_data(), status=404, mimetype='application/json')

    @staticmethod
    def get_all_bids(db_session=None):
        """
        Retrieves a list of all bids.

        Args:
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object containing the list of bids.
        """
        bids = BidMapper.get_all_bids(db_session=db_session)
        data = {"message": "Bids found", "bids": bids}
        return Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')
