from flask import jsonify, Response

from ..data_mappers import ListMapper, ListingMapper


class ListService:
    @staticmethod
    def get_lists(user_id, db_session=None):
        """
        Retrieves a user's lists
        """
        lists = ListMapper.get_lists(user_id=user_id, db_session=db_session)

        if not lists:
            data = {"error": "Lists not found"}
            return Response(response=jsonify(data).get_data(), status=404, mimetype='application/json')

        data = {"message": "Lists found", "lists": lists}
        return Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')


    @staticmethod
    def get_list_items(list_id, db_session=None):
        """
        Retrieves a user's list items
        """
        list_items = ListMapper.get_list_items(list_id=list_id, db_session=db_session)

        if not list_items:
            data = {"error": "List items not found"}
            return Response(response=jsonify(data).get_data(), status=404, mimetype='application/json')

        for i in range(len(list_items)):
            list_items[i] = ListingMapper.get_listing_by_id(listing_id=list_items[i]["listing_id"], db_session=db_session)

        data = {"message": "List items found", "list_items": list_items}
        return Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')


    @staticmethod
    def create_list(data, db_session=None):
        """
        Create a user's list
        """
        list_id = ListMapper.create_list(data=data, db_session=db_session)

        if not list_id:
            data = {"error": "Error creating list"}
            return Response(response=jsonify(data).get_data(), status=404, mimetype='application/json')

        data = {"message": "List created", "list_id": list_id}
        return Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')


    @staticmethod
    def create_list_item(list_id, listing_id, db_session=None):
        """
        Create a user's list item
        """
        list_item_id = ListMapper.create_list_item(list_id=list_id, listing_id=listing_id, db_session=db_session)

        if not list_item_id:
            data = {"error": "Error creating list item"}
            return Response(response=jsonify(data).get_data(), status=404, mimetype='application/json')

        data = {"message": "List item created", "list_item_id": list_item_id}
        return Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')


    @staticmethod
    def update_list(list_id, data, db_session=None):
        """
        Update a user's list
        """
        current_list_items = {item["listing_id"] for item in ListMapper.get_list_items(list_id=list_id, db_session=db_session)}
        updated_list_items = {item["listing_id"] for item in data.get("list_items")}

        if current_list_items == updated_list_items and not data.get("title"):
            data = {"error": "Error updating list"}
            return Response(response=jsonify(data).get_data(), status=400, mimetype="application/json")

        if current_list_items != updated_list_items:
            old_list_items = current_list_items - updated_list_items
            for listing_id in old_list_items:
                deleted_rows = ListMapper.delete_list_item(list_id=list_id, listing_id=listing_id)
                if not deleted_rows:
                    data = {"error": "List item not found"}
                    return Response(response=jsonify(data).get_data(), status=404, mimetype="application/json")

            new_list_items = updated_list_items - current_list_items
            for listing_id in new_list_items:
                created_rows = ListMapper.create_list_item(list_id=list_id, listing_id=listing_id)
                if not created_rows:
                    data = {"error": "Error creating list item"}
                    return Response(response=jsonify(data).get_data(), status=404, mimetype="application/json")

            data = {"message": "List items updated"}
            return Response(response=jsonify(data).get_data(), status=200, mimetype="application/json")

        else:
            updated_rows = ListMapper.update_list(list_id=list_id, title=data.get("title"), db_session=db_session)

            if not updated_rows:
                data = {"error": "List not found"}
                return Response(response=jsonify(data).get_data(), status=404, mimetype="application/json")

            data = {"message": "List updated", "updated_rows": updated_rows}
            return Response(response=jsonify(data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def delete_list(list_id, db_session=None):
        """
        Delete a user's list
        """
        deleted_rows = ListMapper.delete_list(list_id=list_id, db_session=db_session)

        if not deleted_rows:
            data = {"error": "List not found"}
            return Response(response=jsonify(data).get_data(), status=404, mimetype="application/json")

        data = {"message": "List deleted", "deleted_rows": deleted_rows}
        return Response(response=jsonify(data).get_data(), status=200, mimetype="application/json")