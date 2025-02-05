from flask import Blueprint, request, jsonify
from ..services import CategoryService

# Blueprint
category_bp = Blueprint('category_bp', __name__)

#POST /api/categories
@category_bp.route('/', methods=['POST'])
def createCategory():
    data = request.json
    new_category = CategoryService.create_category(data)
    return jsonify(new_category), 201

#GET /api/categories
@category_bp.route('/', methods=['GET'])
def getAllCategories():
    categories = CategoryService.get_all_categories()
    return jsonify(categories), 200

#PUT /api/categories/{id}
@category_bp.route('/<int:category_id', methods=['PUT'])
def updateCategory(category_id):
    data = request.json
    updated_category = CategoryService.update_category(category_id, data)
    if updated_category:
        return jsonify(updated_category), 200
    return jsonify({"error": "Listing not found or update failed"}), 404

#DELETE /api/categories/{id}
@category_bp.route('/<int:category_id>', methods=['DELETE'])
def deleteCategory(category_id):
    success = CategoryService.delete_category(category_id)
    if success:
        return jsonify({"message": "Listing deleted"}), 200
    return jsonify({"error": "Listing not found"}), 404