from flask import Blueprint, request

from ..services.category_services import CategoryService

# Blueprint for category-related routes
category_bp = Blueprint('category_bp', __name__)


# GET /api/categories
@category_bp.route('/', methods=['GET'])
def get_all_categories(db_session=None):
    """Retrieve all categories.

    Args:
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response containing a list of all categories.
    """
    return CategoryService.get_all_categories(db_session=db_session)


# GET /api/categories/{id}
@category_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id, db_session=None):
    """Retrieve a single category by its ID.

    Args:
        category_id (int): The ID of the category to retrieve.
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response containing category details.
    """
    return CategoryService.get_category_by_id(category_id, db_session=db_session)


# POST /api/categories
@category_bp.route('/', methods=['POST'])
def create_category(db_session=None):
    """Create a new category.

    Args:
        db_session: Optional database session to be used in tests.

    Expects:
        JSON payload with category details.

    Returns:
        JSON response containing the created category.
    """
    data = request.json
    return CategoryService.create_category(data, db_session=db_session)


# PUT /api/categories/{id}
@category_bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id, db_session=None):
    """Update an existing category by its ID.

    Args:
        category_id (int): The ID of the category to update.
        db_session: Optional database session to be used in tests.

    Expects:
        JSON payload with updated category details.

    Returns:
        JSON response containing the updated category.
    """
    data = request.json
    return CategoryService.update_category(category_id, data, db_session=db_session)


# DELETE /api/categories/{id}
@category_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id, db_session=None):
    """Delete a category by its ID.

    Args:
        category_id (int): The ID of the category to delete.
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response indicating the deletion status.
    """
    return CategoryService.delete_category(category_id, db_session=db_session)
