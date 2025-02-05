from flask import Blueprint, request, jsonify
from ..services import CategoryService

# Blueprint
category_bp = Blueprint('category_bp', __name__)

#POST /api/categories
@category_bp.route('/', methods=['POST'])
def createCategory():
    data = request.json
    return CategoryService.create_category(data)

#GET /api/categories
@category_bp.route('/', methods=['GET'])
def getAllCategories():
    return CategoryService.get_all_categories()

#PUT /api/categories/{id}
@category_bp.route('/<int:category_id', methods=['PUT'])
def updateCategory(category_id):
    data = request.json
    return CategoryService.update_category(category_id, data)

#DELETE /api/categories/{id}
@category_bp.route('/<int:category_id>', methods=['DELETE'])
def deleteCategory(category_id):
    return CategoryService.delete_category(category_id)