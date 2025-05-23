from flask import Blueprint, request, jsonify, Response
from flask_login import login_required, current_user

from ..services import CategoryService
from ..utils.logger import setup_logger

# Blueprint for category-related routes
bp = Blueprint("category_bp", __name__, url_prefix="/api/categories")

logger = setup_logger(name="category_logger", log_file="logs/category.log")


# GET /api/categories/
@bp.route("/", methods=["GET"])
def get_all_categories(db_session=None):
    """
    Retrieve all categories.

    Args:
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response containing a list of all categories.
    """
    return CategoryService.get_all_categories(db_session=db_session)


# GET /api/categories/{id}/
@bp.route("/<int:category_id>/", methods=["GET"])
def get_category(category_id: int, db_session=None):
    """
    Retrieve a single category by its ID.

    Args:
        category_id (int): The ID of the category to retrieve.
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response containing category details.
    """
    return CategoryService.get_category_by_id(category_id=category_id, db_session=db_session)


# POST /api/categories/
@bp.route("/", methods=["POST"])
@login_required
def create_category(db_session=None):
    """
    Create a new category.

    Args:
        db_session: Optional database session to be used in tests.

    Expects:
        JSON payload with category details.

    Returns:
        JSON response containing the created category.
    """
    if current_user.role not in ["staff", "admin"]:
        response_data = {"error": "Unauthorized access"}
        logger.error(msg=f"Unauthorized access attempt to create category by user {current_user.id}")
        return Response(response=jsonify(response_data).get_data(), status=401, mimetype="application/json")

    data = request.json
    return CategoryService.create_category(data=data, db_session=db_session)


# PUT /api/categories/{id}/
@bp.route("/<int:category_id>/", methods=["PUT"])
@login_required
def update_category(category_id: int, db_session=None):
    """
    Update an existing category by its ID.

    Args:
        category_id (int): The ID of the category to update.
        db_session: Optional database session to be used in tests.

    Expects:
        JSON payload with updated category details.

    Returns:
        JSON response containing the updated category.
    """
    if current_user.role not in ["staff", "admin"]:
        response_data = {"error": "Unauthorized access"}
        logger.error(msg=f"Unauthorized access attempt to update category by user {current_user.id}")
        return Response(response=jsonify(response_data).get_data(), status=401, mimetype="application/json")

    data = request.json
    return CategoryService.update_category(category_id=category_id, data=data, db_session=db_session)


# DELETE /api/categories/{id}/
@bp.route("/<int:category_id>/", methods=["DELETE"])
@login_required
def delete_category(category_id: int, db_session=None):
    """
    Delete a category by its ID.

    Args:
        category_id (int): The ID of the category to delete.
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response indicating the deletion status.
    """
    if current_user.role not in ["staff", "admin"]:
        response_data = {"error": "Unauthorized access"}
        logger.error(msg=f"Unauthorized access attempt to delete category by user {current_user.id}")
        return Response(response=jsonify(response_data).get_data(), status=401, mimetype="application/json")
    
    return CategoryService.delete_category(category_id=category_id, db_session=db_session)
