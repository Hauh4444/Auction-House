from flask import Blueprint, request

from ..services.categories import CategoryService

# Blueprint for category-related routes
category_bp = Blueprint('category_bp', __name__)


# GET /api/categories
@category_bp.route('/', methods=['GET'])
def get_all_categories():
    """Retrieve all categories.

    Returns:
        JSON response containing a list of all categories.
    """
    return CategoryService.get_all_categories()


# GET /api/categories/{id}
@category_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Retrieve a single category by its ID.

    Args:
        category_id (int): The ID of the category to retrieve.

    Returns:
        JSON response containing category details.
    """
    return CategoryService.get_category_by_id(category_id)


# POST /api/categories
@category_bp.route('/', methods=['POST'])
def createCategory():
    """Create a new category.

    Expects:
        JSON payload with category details.

    Returns:
        JSON response containing the created category.
    """
    data = request.json
    return CategoryService.create_category(data)


# PUT /api/categories/{id}
@category_bp.route('/<int:category_id>', methods=['PUT'])
def updateCategory(category_id):
    """Update an existing category by its ID.

    Args:
        category_id (int): The ID of the category to update.

    Expects:
        JSON payload with updated category details.

    Returns:
        JSON response containing the updated category.
    """
    data = request.json
    return CategoryService.update_category(category_id, data)


# DELETE /api/categories/{id}
@category_bp.route('/<int:category_id>', methods=['DELETE'])
def deleteCategory(category_id):
    """Delete a category by its ID.

    Args:
        category_id (int): The ID of the category to delete.

    Returns:
        JSON response indicating the deletion status.
    """
    return CategoryService.delete_category(category_id)
