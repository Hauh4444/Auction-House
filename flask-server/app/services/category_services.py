from flask import jsonify
from ..data_mappers.category_mappers import CategoryMapper


class CategoryService:
    @staticmethod
    def get_all_categories():
        """
        Retrieves a list of all categories.

        Returns:
            A JSON response containing the list of categories with a 200 status code.
        """
        categories = CategoryMapper.get_all_categories()
        return jsonify(categories), 200

    @staticmethod
    def get_category_by_id(category_id):
        """
        Retrieves a specific category by its ID.

        Args:
            category_id: The ID of the category to retrieve.

        Returns:
            A JSON response with the category data if found, otherwise a 404 error with a message.
        """
        category = CategoryMapper.get_category_by_id(category_id)
        if category:
            return jsonify(category), 200
        return jsonify({"error": "CategoryNav not found"}), 404

    @staticmethod
    def create_category(data):
        """
        Creates a new category with the provided data.

        Args:
            data: A dictionary containing the category details such as name, description, etc.

        Returns:
            A JSON response with the success message and newly created category ID, or a 400 error if the name is missing.
        """
        if not data.get("name"):
            return jsonify({"error": "CategoryNav name is required"}), 400
        category_id = CategoryMapper.create_category(data)
        return jsonify({"message": "CategoryNav created", "category_id": category_id}), 201

    @staticmethod
    def update_category(category_id, data):
        """
        Updates an existing category by its ID with the provided data.

        Args:
            category_id: The ID of the category to update.
            data: A dictionary containing the fields to update.

        Returns:
            A JSON response with a success message if the category was updated, or a 404 error if the category was not found.
        """
        updated_rows = CategoryMapper.update_category(category_id, data)
        if updated_rows:
            return jsonify({"message": "CategoryNav updated"}), 200
        return jsonify({"error": "CategoryNav not found"}), 404

    @staticmethod
    def delete_category(category_id):
        """
        Deletes a category by its ID.

        Args:
            category_id: The ID of the category to delete.

        Returns:
            A JSON response with a success message if the category was deleted, or a 404 error if the category was not found.
        """
        deleted_rows = CategoryMapper.delete_category(category_id)
        if deleted_rows:
            return jsonify({"message": "CategoryNav deleted"}), 200
        return jsonify({"error": "CategoryNav not found"}), 404
