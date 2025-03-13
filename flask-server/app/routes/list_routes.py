from flask import Blueprint, request, session
from flask_login import login_required

from ..services import ListService

# Blueprint for list-related routes
bp = Blueprint("list_bp", __name__, url_prefix="/api/user/lists")


# GET /api/user/lists
@bp.route('/', methods=['GET'])
@login_required
def get_lists(db_session=None):
    """
    Retrieve a user's lists.
    """
    user_id = session["user_id"]
    return ListService.get_lists(user_id=user_id, db_session=db_session)


# GET /api/user/lists/{id}
@bp.route('/<int:list_id>', methods=['GET'])
@login_required
def get_list_items(list_id, db_session=None):
    """
    Retrieve a user's list items.
    """
    return ListService.get_list_items(list_id=list_id, db_session=db_session)


# POST /api/user/lists
@bp.route('/', methods=['POST'])
@login_required
def create_list(db_session=None):
    """
    Create a user's list
    """
    data = request.json
    data["user_id"] = session["user_id"]
    return ListService.create_list(data=data, db_session=db_session)


# POST /api/user/lists/{id}
@bp.route('/<int:list_id>', methods=['POST'])
@login_required
def create_list_item(list_id, db_session=None):
    """
    Create a user's list item
    """
    data = request.json
    listing_id = data.get("listing_id")
    return ListService.create_list_item(list_id=list_id, listing_id=listing_id, db_session=db_session)


# PUT /api/user/lists/{id}
@bp.route('/<int:list_id>', methods=['PUT'])
@login_required
def update_list(list_id, db_session=None):
    """
    Update a user's list
    """
    data = request.json
    return ListService.update_list(list_id=list_id, data=data, db_session=db_session)


# DELETE /api/user/lists/{id}
@bp.route('/<int:list_id>', methods=['DELETE'])
@login_required
def delete_list(list_id, db_session=None):
    """
    Delete a user's list
    """
    return ListService.delete_list(list_id=list_id, db_session=db_session)