from flask import jsonify

from ..data_mappers import CategoryMapper


class CategoryService:
    @staticmethod
    def get_all_categories(db_session=None):
        """
        Retrieves a list of all categories.

        Args:
            db_session: Optional database session to be used in tests.

        Returns:
            A JSON response containing the list of categories with a 200 status code.
        """
        categories = CategoryMapper.get_all_categories(db_session=db_session)
        return jsonify(categories), 200

    @staticmethod
    def get_category_by_id(category_id, db_session=None):
        """
        Retrieves a specific category by its ID.

        Args:
            category_id: The ID of the category to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            A JSON response with the category data if found, otherwise a 404 error with a message.
        """
        category = CategoryMapper.get_category_by_id(category_id=category_id, db_session=db_session)
        if category:
            return jsonify(category), 200
        return jsonify({"error": "CategoryNav not found"}), 404

    @staticmethod
    def create_category(data, db_session=None):
        """
        Creates a new category with the provided data.

        Args:
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A JSON response with the success message and newly created category ID, or a 400 error if the name is missing.
        """
        if not data.get("name"):
            return jsonify({"error": "CategoryNav name is required"}), 400
        category_id = CategoryMapper.create_category(data=data, db_session=db_session)
        return jsonify({"message": "CategoryNav created", "category_id": category_id}), 201

    @staticmethod
    def update_category(category_id, data, db_session=None):
        """
        Updates an existing category by its ID with the provided data.

        Args:
            category_id: The ID of the category to update.
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A JSON response with a success message if the category was updated, or a 404 error if the category was not found.
        """
        updated_rows = CategoryMapper.update_category(category_id=category_id, data=data, db_session=db_session)
        if updated_rows:
            return jsonify({"message": "CategoryNav updated"}), 200
        return jsonify({"error": "CategoryNav not found"}), 404

    @staticmethod
    def delete_category(category_id, db_session=None):
        """
        Deletes a category by its ID.

        Args:
            category_id: The ID of the category to delete.
            db_session: Optional database session to be used in tests.

        Returns:
            A JSON response with a success message if the category was deleted, or a 404 error if the category was not found.
        """
        deleted_rows = CategoryMapper.delete_category(category_id=category_id, db_session=db_session)
        if deleted_rows:
            return jsonify({"message": "CategoryNav deleted"}), 200
        return jsonify({"error": "CategoryNav not found"}), 404
