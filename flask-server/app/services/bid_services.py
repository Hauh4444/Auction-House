from flask import jsonify, Response

from ..data_mappers import BidMapper, ListingMapper
from ..utils.socketio import socketio


class BidService:
    @staticmethod
    def get_all_bids(db_session=None):
        """
        Retrieves a list of all bids.

        Args:
            db_session (Optional[Session]): An optional database session to be used in tests.

        Returns:
            Response: A JSON response containing the list of all bids.
        """
        bids = BidMapper.get_all_bids(db_session=db_session)
        if not bids:
            response_data = {"error": "No bids found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Bids found", "bids": bids}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def get_bid_by_id(bid_id, db_session=None):
        """
        Retrieves a specific bid by its ID.

        Args:
            bid_id (int): The ID of the bid to retrieve.
            db_session (Optional[Session]): An optional database session to be used in tests.

        Returns:
            Response: A JSON response containing the bid data if found.
                Returns status code 404 if the bid is not found.
        """
        bid = BidMapper.get_bid_by_id(bid_id=bid_id, db_session=db_session)
        if not bid:
            response_data = {"error": "Bid not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Bid found", "bid": bid}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")



    @staticmethod
    def create_bid(data, db_session=None):
        """
        Creates a new bid and emits an event through a socket.

        Args:
            data (dict): A dictionary containing the bid details (e.g., user, amount).
            db_session (Optional[Session]): An optional database session used for testing.

        Returns:
            Response: A JSON response containing the success message, bid ID, and bid data if successful.
                Returns status code 400 if required fields are missing.
        """
        # Validation to check if required fields are present
        if not data.get("user") or not data.get("amount"):
            response_data = {"error": "User and amount are required"}
            return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")

        bid_id = BidMapper.create_bid(data=data, db_session=db_session)
        if not bid_id:
            response_data = {"error": "Error creating bid"}
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

        listing_update_data = {"bids": "bids + 1"}
        updated_rows = ListingMapper.update_listing(listing_id=data.get("listing_id"), data=listing_update_data, db_session=db_session)
        if not updated_rows:
            response_data = {"error": "Error updating listing"}
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

        bid = BidMapper.get_bid_by_id(bid_id=bid_id, db_session=db_session)
        if not bid:
            response_data = {"error": "Bid not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        socketio.emit('new_bid', {"data": data})

        response_data = {"message": "Bid created", "bid_id": bid_id}
        return Response(response=jsonify(response_data).get_data(), status=201, mimetype="application/json")