from flask import jsonify, Response

from ..data_mappers import CategoryMapper


class CategoryService:
    @staticmethod
    def get_all_categories(db_session=None):
        """
        Retrieves a list of all categories.

        Args:
            db_session (Optional[Session]): An optional database session to be used in tests.

        Returns:
            Response: A JSON response containing the list of categories.
                Returns status code 404 if no categories are found.
        """
        categories = CategoryMapper.get_all_categories(db_session=db_session)
        if not categories:
            response_data = {"error": "No categories found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Categories found", "categories": categories}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")

    @staticmethod
    def get_category_by_id(category_id, db_session=None):
        """
        Retrieves a specific category by its ID.

        Args:
            category_id (int): The ID of the category to retrieve.
            db_session (Optional[Session]): An optional database session to be used in tests.

        Returns:
            Response: A JSON response containing the category data if found.
                Returns status code 404 if the category is not found.
        """
        category = CategoryMapper.get_category_by_id(category_id=category_id, db_session=db_session)
        if not category:
            response_data = {"error": "Category not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Category found", "category": category}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")

    @staticmethod
    def create_category(data, db_session=None):
        """
        Creates a new category with the provided data.

        Args:
            data (dict): A dictionary containing the category details (e.g., name).
            db_session (Optional[Session]): An optional database session to be used in tests.

        Returns:
            Response: A JSON response with the success message and newly created category ID.
                Returns status code 409 if there was an error creating the category.
        """
        category_id = CategoryMapper.create_category(data=data, db_session=db_session)
        if not category_id:
            response_data = {"error": "Error creating category"}
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

        response_data = {"message": "Category created", "category_id": category_id}
        return Response(response=jsonify(response_data).get_data(), status=201, mimetype="application/json")

    @staticmethod
    def update_category(category_id, data, db_session=None):
        """
        Updates an existing category by its ID with the provided data.

        Args:
            category_id (int): The ID of the category to update.
            data (dict): A dictionary containing the updated category details.
            db_session (Optional[Session]): An optional database session to be used in tests.

        Returns:
            Response: A JSON response with a success message if the category was updated.
                Returns status code 409 if the category was not updated.
        """
        updated_rows = CategoryMapper.update_category(category_id=category_id, data=data, db_session=db_session)
        if not updated_rows:
            response_data = {"error": "Error updating category"}
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

        response_data = {"message": "Category updated", "updated_rows": updated_rows}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")

    @staticmethod
    def delete_category(category_id, db_session=None):
        """
        Deletes a category by its ID.

        Args:
            category_id (int): The ID of the category to delete.
            db_session (Optional[Session]): An optional database session to be used in tests.

        Returns:
            Response: A JSON response with a success message if the category was deleted.
                Returns status code 404 if the category was not found.
        """
        deleted_rows = CategoryMapper.delete_category(category_id=category_id, db_session=db_session)
        if not deleted_rows:
            response_data = {"error": "Category not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Category deleted", "deleted_rows": deleted_rows}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")
