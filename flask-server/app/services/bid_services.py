from flask import jsonify, Response

from ..data_mappers import BidMapper, ListingMapper
from ..utils.socketio import socketio
from ..utils.logger import setup_logger

logger = setup_logger(name="bid_logger", log_file="logs/bid.log")


class BidService:
    @staticmethod
    def get_all_bids(db_session=None):
        """
        Retrieves a list of all bids.

        Args:
            db_session: Optional database session to be used in tests.

        Returns:
            Response: A JSON response containing the list of all bids.
        """
        bids = BidMapper.get_all_bids(db_session=db_session)
        if not bids:
            response_data = {"error": "No bids found"}
            logger.error(msg=f"No bids found")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Bids found", "bids": bids}
        logger.info(msg=f"Bids found: {[bid.get('bid_id') for bid in bids]}")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def get_bid_by_id(bid_id: int, db_session=None):
        """
        Retrieves a specific bid by its ID.

        Args:
            bid_id (int): The ID of the bid to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            Response: A JSON response containing the bid data if found.
                Returns status code 404 if the bid is not found.
        """
        bid = BidMapper.get_bid_by_id(bid_id=bid_id, db_session=db_session)
        if not bid:
            response_data = {"error": "Bid not found"}
            logger.error(msg=f"Bid: {bid_id} not found")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Bid found", "bid": bid}
        logger.info(msg=f"Bid: {bid_id} found")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")



    @staticmethod
    def create_bid(data: dict, db_session=None):
        """
        Creates a new bid and emits an event through a socket.

        Args:
            data (dict): A dictionary containing the bid details (e.g., user, amount).
            db_session: Optional database session to be used in tests.

        Returns:
            Response: A JSON response containing the success message, bid ID, and bid data if successful.
                Returns status code 400 if required fields are missing.
        """
        bid_id = BidMapper.create_bid(data=data, db_session=db_session)
        if not bid_id:
            response_data = {"error": "Error creating bid"}
            logger.error(msg=f"Failed creating bid with data: {', '.join(f'{k}={v!r}' for k, v in data.items())}")
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

        listing_args = {"bids": 1, "current_price": data.get("amount")}
        updated_rows = ListingMapper.update_listing(listing_id=data.get("listing_id"), data=listing_args, db_session=db_session)
        if not updated_rows:
            response_data = {"error": "Error updating listing"}
            logger.error(msg=f"Failed updating listing with data: {', '.join(f'{k}={v!r}' for k, v in listing_args.items())}")
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

        bid = BidMapper.get_bid_by_id(bid_id=bid_id, db_session=db_session)
        if not bid:
            response_data = {"error": "Bid not found"}
            logger.error(msg=f"Bid: {bid_id} not found")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        socketio.emit("new_bid")

        response_data = {"message": "Bid created", "bid_id": bid_id}
        logger.info(msg=f"Bid: {bid_id} created successfully with data: {', '.join(f'{k}={v!r}' for k, v in data.items())}")
        return Response(response=jsonify(response_data).get_data(), status=201, mimetype="application/json")