from flask import jsonify, Response

from ..data_mappers import ListMapper


class ListService:
    @staticmethod
    def get_user_list_items(list_id, db_session=None):
        """
        Retrieves a user's orders

        Args:
            list_id (int): The ID of the list to retrieve items of.
            db_session: Optional database session to be used in tests.

        Returns:
            A response object with the list items data if found, otherwise a 404 error with a message.
        """
        list_items = ListMapper.get_all_list_items(list_id=list_id, db_session=db_session)

        if list_items:
            data = {"message": "List items found", "list_items": list_items}
            return Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')

        data = {"error": "List items not found"}
        return Response(response=jsonify(data).get_data(), status=404, mimetype='application/json')


    @staticmethod
    def get_user_lists(user_id, db_session=None):
        """
        Retrieves a user's orders

        Args:
            user_id (int): The ID of the user to retrieve history of.
            db_session: Optional database session to be used in tests.

        Returns:
            A response object with the lists data if found, otherwise a 404 error with a message.
        """
        lists = ListMapper.get_all_lists(user_id=user_id, db_session=db_session)

        if lists:
            data = {"message": "Lists found", "lists": lists}
            return Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')

        data = {"error": "Lists not found"}
        return Response(response=jsonify(data).get_data(), status=404, mimetype='application/json')