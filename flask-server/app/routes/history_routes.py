from flask import Blueprint, request, jsonify, Response
from flask_login import login_required, current_user

from ..services import HistoryService
from ..utils.logger import setup_logger

# Blueprint for history-related routes
bp = Blueprint("history_bp", __name__, url_prefix="/api/user")

logger = setup_logger(name="history_logger", log_file="logs/history.log")


# GET /api/user/orders/
@bp.route('/orders/', methods=['GET'])
@login_required
def get_user_orders(db_session=None):
    """
    Retrieve a user's order history.

    Args:
        db_session (optional): A database session for testing or direct queries.

    Returns:
        JSON response containing a list of the user's past orders.
    """
    data = None
    if current_user.role in ["staff", "admin"]:
        data = request.args.to_dict()

    return HistoryService.get_user_orders(data=data, db_session=db_session)


# PUT /api/user/orders/<int:order_id>/
@bp.route('/orders/<int:order_id>/', methods=['PUT'])
@login_required
def update_user_order(order_id, db_session=None):
    """
    Update a specific order in the user's history.
    """
    if current_user.role not in ["staff", "admin"]:
        response_data = {"error": "Unauthorized access"}
        logger.error(msg=f"Unauthorized access attempt to update order by user {current_user.id}")
        return Response(response=jsonify(response_data).get_data(), status=401, mimetype="application/json")

    data = request.json
    return HistoryService.update_user_order(order_id=order_id, data=data, db_session=db_session)


# DELETE /api/user/orders/<int:order_id>/
@bp.route('/orders/<int:order_id>/', methods=['DELETE'])
@login_required
def delete_user_order(order_id, db_session=None):
    """
    Delete a specific order from the user's history.
    """
    if current_user.role not in ["staff", "admin"]:
        response_data = {"error": "Unauthorized access"}
        logger.error(msg=f"Unauthorized access attempt to delete order by user {current_user.id}")
        return Response(response=jsonify(response_data).get_data(), status=401, mimetype="application/json")

    return HistoryService.delete_user_order(order_id=order_id, db_session=db_session)


# GET /api/user/listings/
@bp.route('/listings/', methods=['GET'])
@login_required
def get_user_listings(db_session=None):
    """
    Retrieve a user's listing history.

    Args:
        db_session (optional): A database session for testing or direct queries.

    Returns:
        JSON response containing a list of the user's past listings.
    """
    data = None
    if current_user.role in ["staff", "admin"]:
        data = request.args.to_dict()

    return HistoryService.get_user_listings(data=data, db_session=db_session)


# PUT /api/user/listings/<int:listing_id>/
@bp.route('/listings/<int:listing_id>/', methods=['PUT'])
@login_required
def update_user_listing(listing_id, db_session=None):
    """
    Update a specific listing in the user's history.
    """
    data = request.json
    return HistoryService.update_user_listing(listing_id=listing_id, data=data, db_session=db_session)


# DELETE /api/user/listings/<int:listing_id>/
@bp.route('/listings/<int:listing_id>/', methods=['DELETE'])
@login_required
def delete_user_listing(listing_id, db_session=None):
    """
    Delete a specific listing from the user's history.
    """
    return HistoryService.delete_user_listing(listing_id=listing_id, db_session=db_session)


# GET /api/user/transactions/
@bp.route('/transactions/', methods=['GET'])
@login_required
def get_user_transactions(db_session=None):
    """
    Retrieve a user's transaction history.

    Args:
        db_session (optional): A database session for testing or direct queries.

    Returns:
        JSON response containing a list of the user's past transactions.
    """
    data = None
    if current_user.role in ["staff", "admin"]:
        data = request.args.to_dict()

    return HistoryService.get_user_transactions(data=data, db_session=db_session)


# PUT /api/user/transactions/<int:transaction_id>/
@bp.route('/transactions/<int:transaction_id>/', methods=['PUT'])
@login_required
def update_user_transaction(transaction_id, db_session=None):
    """
    Update a specific transaction in the user's history.
    """
    if current_user.role not in ["staff", "admin"]:
        response_data = {"error": "Unauthorized access"}
        logger.error(msg=f"Unauthorized access attempt to update transaction by user {current_user.id}")
        return Response(response=jsonify(response_data).get_data(), status=401, mimetype="application/json")

    data = request.json
    return HistoryService.update_user_transaction(transaction_id=transaction_id, data=data, db_session=db_session)


# DELETE /api/user/transactions/<int:transaction_id>/
@bp.route('/transactions/<int:transaction_id>/', methods=['DELETE'])
@login_required
def delete_user_transaction(transaction_id, db_session=None):
    """
    Delete a specific transaction from the user's history.
    """
    if current_user.role not in ["staff", "admin"]:
        response_data = {"error": "Unauthorized access"}
        logger.error(msg=f"Unauthorized access attempt to delete transaction by user {current_user.id}")
        return Response(response=jsonify(response_data).get_data(), status=401, mimetype="application/json")

    return HistoryService.delete_user_transaction(transaction_id=transaction_id, db_session=db_session)


# GET /api/user/deliveries/
@bp.route('/deliveries/', methods=['GET'])
@login_required
def get_user_deliveries(db_session=None):
    """
    Retrieve a user's delivery history.

    Args:
        db_session (optional): A database session for testing or direct queries.

    Returns:
        JSON response containing a list of the user's past deliveries.
    """
    data = None
    if current_user.role in ["staff", "admin"]:
        data = request.args.to_dict()

    return HistoryService.get_user_deliveries(data=data, db_session=db_session)


# PUT /api/user/deliveries/<int:delivery_id>/
@bp.route('/deliveries/<int:delivery_id>/', methods=['PUT'])
@login_required
def update_user_delivery(delivery_id, db_session=None):
    """
    Update a specific delivery in the user's history.
    """
    if current_user.role not in ["staff", "admin"]:
        response_data = {"error": "Unauthorized access"}
        logger.error(msg=f"Unauthorized access attempt to update delivery by user {current_user.id}")
        return Response(response=jsonify(response_data).get_data(), status=401, mimetype="application/json")

    data = request.json
    return HistoryService.update_user_delivery(delivery_id=delivery_id, data=data, db_session=db_session)


# DELETE /api/user/deliveries/<int:delivery_id>/
@bp.route('/deliveries/<int:delivery_id>/', methods=['DELETE'])
@login_required
def delete_user_delivery(delivery_id, db_session=None):
    """
    Delete a specific delivery from the user's history.
    """
    if current_user.role not in ["staff", "admin"]:
        response_data = {"error": "Unauthorized access"}
        logger.error(msg=f"Unauthorized access attempt to delete delivery by user {current_user.id}")
        return Response(response=jsonify(response_data).get_data(), status=401, mimetype="application/json")

    return HistoryService.delete_user_delivery(delivery_id=delivery_id, db_session=db_session)


# GET /api/user/support-tickets/
@bp.route('/support-tickets/', methods=['GET'])
@login_required
def get_user_support_tickets(db_session=None):
    """
    Retrieve a user's support ticket history.

    Args:
        db_session (optional): A database session for testing or direct queries.

    Returns:
        JSON response containing a list of the user's past support tickets.
    """
    data = None
    if current_user.role in ["staff", "admin"]:
        data = request.args.to_dict()

    return HistoryService.get_user_support_tickets(data=data, db_session=db_session)


# PUT /api/user/support-tickets/<int:ticket_id>/
@bp.route('/support-tickets/<int:ticket_id>/', methods=['PUT'])
@login_required
def update_user_support_ticket(ticket_id, db_session=None):
    """
    Update a specific support ticket in the user's history.
    """
    if current_user.role not in ["staff", "admin"]:
        response_data = {"error": "Unauthorized access"}
        logger.error(msg=f"Unauthorized access attempt to update support ticket by user {current_user.id}")
        return Response(response=jsonify(response_data).get_data(), status=401, mimetype="application/json")

    data = request.json
    return HistoryService.update_user_support_ticket(ticket_id=ticket_id, data=data, db_session=db_session)


# DELETE /api/user/support-tickets/<int:ticket_id>/
@bp.route('/support-tickets/<int:ticket_id>/', methods=['DELETE'])
@login_required
def delete_user_support_ticket(ticket_id, db_session=None):
    """
    Delete a specific support ticket from the user's history.
    """
    if current_user.role not in ["staff", "admin"]:
        response_data = {"error": "Unauthorized access"}
        logger.error(msg=f"Unauthorized access attempt to delete support ticket by user {current_user.id}")
        return Response(response=jsonify(response_data).get_data(), status=401, mimetype="application/json")

    return HistoryService.delete_user_support_ticket(ticket_id=ticket_id, db_session=db_session)


# GET /api/user/reviews/
@bp.route('/reviews/', methods=['GET'])
@login_required
def get_user_reviews(db_session=None):
    """
    Retrieve a user's review history.

    Args:
        db_session (optional): A database session for testing or direct queries.

    Returns:
        JSON response containing a list of the user's past reviews.
    """
    data = None
    if current_user.role in ["staff", "admin"]:
        data = request.args.to_dict()

    return HistoryService.get_user_reviews(data=data, db_session=db_session)


# PUT /api/user/reviews/<int:review_id>/
@bp.route('/reviews/<int:review_id>/', methods=['PUT'])
@login_required
def update_user_review(review_id, db_session=None):
    """
    Update a specific review in the user's history.
    """
    data = request.json
    return HistoryService.update_user_review(review_id=review_id, data=data, db_session=db_session)


# DELETE /api/user/reviews/<int:review_id>/
@bp.route('/reviews/<int:review_id>/', methods=['DELETE'])
@login_required
def delete_user_review(review_id, db_session=None):
    """
    Delete a specific review from the user's history.
    """
    return HistoryService.delete_user_review(review_id=review_id, db_session=db_session)