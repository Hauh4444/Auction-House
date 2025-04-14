from flask import jsonify, Response, session
from flask_login import current_user

from ..data_mappers import ListMapper, ListingMapper
from ..utils.logger import setup_logger

list_logger = setup_logger("list", "logs/list.log")


class ListService:
    @staticmethod
    def get_lists(db_session=None):
        """
        Retrieve User Lists

        Args:
            db_session (optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response containing the user's lists if found, otherwise a 404 error.
        """
        lists = ListMapper.get_lists(user_id=session.get("user_id"), db_session=db_session)

        if not lists:
            response_data = {"error": "Lists not found"}
            list_logger.error("All lists not found! User ID: " + current_user.id)
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Lists found", "lists": lists}
        list_logger.info("Lists found by user: " + current_user.id)
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')


    @staticmethod
    def get_list_items(list_id, db_session=None):
        """
        Retrieve Items in a List

        Args:
            list_id (int): The ID of the list whose items are being retrieved.
            db_session (optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response containing the list items if found, otherwise a 404 error.
        """
        list_items = ListMapper.get_list_items(list_id=list_id, db_session=db_session)

        if not list_items:
            response_data = {"error": "List items not found"}
            list_logger.error("List item with id " + list_id + " was not found. User: " + current_user.id)
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        for i in range(len(list_items)):
            list_items[i] = ListingMapper.get_listing_by_id(listing_id=list_items[i].get("listing_id"), db_session=db_session)

        response_data = {"message": "List items found", "list_items": list_items}
        list_logger.info("List item with id " + list_id + " not found. User: " + current_user.id)
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')


    @staticmethod
    def create_list(data, db_session=None):
        """
        Create a New List

        Args:
            data (dict): The data required to create the list, including the user ID and title.
            db_session (optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response containing the newly created list ID or an error message.
        """
        data.update(user_id=session.get("user_id"))
        list_id = ListMapper.create_list(data=data, db_session=db_session)

        if not list_id:
            response_data = {"error": "Error creating list"}
            list_logger.error("Error creating list using data " + data + " by user " + current_user.id)
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype='application/json')

        response_data = {"message": "List created", "list_id": list_id}
        list_logger.info("Successfully created list " + list_id + " by user " + current_user.id)
        return Response(response=jsonify(response_data).get_data(), status=201, mimetype='application/json')


    @staticmethod
    def create_list_item(list_id, listing_id, db_session=None):
        """
        Add an Item to a List

        Args:
            list_id (int): The ID of the list to which the item will be added.
            listing_id (int): The ID of the listing to be added to the list.
            db_session (optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response containing the newly created list item ID or an error message.
        """
        list_items = ListMapper.get_list_items(list_id=list_id, db_session=db_session)

        for item in list_items:
            if item.get("listing_id") == listing_id:
                response_data = {"error": "Item is already in list"}
                list_logger.error("The item " + listing_id + " already exists in the list")
                return Response(response=jsonify(response_data).get_data(), status=409, mimetype='application/json')

        list_item_id = ListMapper.create_list_item(list_id=list_id, listing_id=listing_id, db_session=db_session)

        if not list_item_id:
            response_data = {"error": "Error creating list item"}
            list_logger.error("Error creating list item by user " + current_user.id)
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype='application/json')

        response_data = {"message": "List item created", "list_item_id": list_item_id}
        list_logger.info("Successfully created list item " + list_item_id + " by user " + current_user.id)
        return Response(response=jsonify(response_data).get_data(), status=201, mimetype='application/json')


    @staticmethod
    def update_list(list_id, data, db_session=None):
        """
        Update an Existing List

        Args:
            list_id (int): The ID of the list to be updated.
            data (dict): The update data containing a new title and/or list items.
            db_session (optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response indicating success or an error message.
        """
        current_list_items = {item.get("listing_id") for item in ListMapper.get_list_items(list_id=list_id, db_session=db_session)}
        updated_list_items = {item.get("listing_id") for item in data.get("list_items")}

        if current_list_items == updated_list_items and not data.get("title"):
            response_data = {"error": "Error updating list"}
            list_logger.error("Error updating list with data: " + data + "\nUser: " + current_user.id)
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

        if current_list_items != updated_list_items:
            old_list_items = current_list_items - updated_list_items
            for listing_id in old_list_items:
                deleted_rows = ListMapper.delete_list_item(list_id=list_id, listing_id=listing_id)

                if not deleted_rows:
                    response_data = {"error": "List item not found"}
                    list_logger.error("Error: List item " + list_id + " not found by user: " + current_user.id)
                    return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

            new_list_items = updated_list_items - current_list_items
            for listing_id in new_list_items:
                created_rows = ListMapper.create_list_item(list_id=list_id, listing_id=listing_id)

                if not created_rows:
                    response_data = {"error": "Error creating list item"}
                    list_logger.error("Error creating list item using data: " + data + "\nUser: " + current_user.id)
                    return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

            response_data = {"message": "List items updated"}
            list_logger.info("List successfully updated: " + updated_rows + "\nUser: " + current_user.id)
            return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")

        else:
            updated_rows = ListMapper.update_list(list_id=list_id, title=data.get("title"), db_session=db_session)

            if not updated_rows:
                response_data = {"error": "List not found"}
                list_logger.error("List not found: " + list_id)
                return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

            response_data = {"message": "List updated", "updated_rows": updated_rows}
            list_logger.info("List successfully updated: " + updated_rows + "\nUser: " + current_user.id)
            return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def delete_list(list_id, db_session=None):
        """
        Delete a List

        Args:
            list_id (int): The ID of the list to be deleted.
            db_session (optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response indicating success or an error message.
        """
        deleted_rows = ListMapper.delete_list(list_id=list_id, db_session=db_session)

        if not deleted_rows:
            response_data = {"error": "List not found"}
            list_logger.error("List id " + list_id + " not found by user: " + current_user.id)
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "List deleted", "deleted_rows": deleted_rows}
        list_logger.info("List successfully deleted " + deleted_rows + " by user: " + current_user.id)
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")
