from flask import Blueprint, request
from flask_login import login_required

from ..services import ListService

# Blueprint for list-related routes
bp = Blueprint("list_bp", __name__, url_prefix="/api/user/lists")


# GET /api/user/lists/
@bp.route('/', methods=['GET'])
@login_required
def get_lists(db_session=None):
    """
    Retrieve all lists created by the authenticated user.

    Args:
        db_session (optional): A database session for testing or direct queries.

    Returns:
        JSON response containing a list of the user's saved lists.
    """
    return ListService.get_lists(db_session=db_session)


# GET /api/user/lists/{id}/
@bp.route('/<int:list_id>/', methods=['GET'])
@login_required
def get_list_items(list_id, db_session=None):
    """
    Retrieve items from a specific user-created list.

    Args:
        list_id (int): The ID of the list.
        db_session (optional): A database session for testing or direct queries.

    Returns:
        JSON response containing a list of items in the specified list.
    """
    return ListService.get_list_items(list_id=list_id, db_session=db_session)


# POST /api/user/lists/
@bp.route('/', methods=['POST'])
@login_required
def create_list(db_session=None):
    """
    Create a new list for the authenticated user.

    Args:
        db_session (optional): A database session for testing or direct queries.

    Returns:
        JSON response containing the newly created list details.
    """
    data = request.json
    return ListService.create_list(data=data, db_session=db_session)


# POST /api/user/lists/{id}/
@bp.route('/<int:list_id>/', methods=['POST'])
@login_required
def create_list_item(list_id, db_session=None):
    """
    Add an item to a specific user-created list.

    Args:
        list_id (int): The ID of the list.
        db_session (optional): A database session for testing or direct queries.

    Returns:
        JSON response confirming the addition of the item to the list.
    """
    data = request.json
    listing_id = data.get("listing_id")
    return ListService.create_list_item(list_id=list_id, listing_id=listing_id, db_session=db_session)


# PUT /api/user/lists/{id}/
@bp.route('/<int:list_id>/', methods=['PUT'])
@login_required
def update_list(list_id, db_session=None):
    """
    Update the details of a user-created list.

    Args:
        list_id (int): The ID of the list to update.
        db_session (optional): A database session for testing or direct queries.

    Returns:
        JSON response confirming the successful update of the list.
    """
    data = request.json
    return ListService.update_list(list_id=list_id, data=data, db_session=db_session)


# DELETE /api/user/lists/{id}/
@bp.route('/<int:list_id>/', methods=['DELETE'])
@login_required
def delete_list(list_id, db_session=None):
    """
    Delete a user-created list.

    Args:
        list_id (int): The ID of the list to delete.
        db_session (optional): A database session for testing or direct queries.

    Returns:
        JSON response confirming the deletion of the list.
    """
    return ListService.delete_list(list_id=list_id, db_session=db_session)
