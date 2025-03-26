from flask import jsonify, Response, session

from ..data_mappers import SupportTicketMapper


class SupportTicketService:
    @staticmethod
    def get_tickets(db_session=None):
        """
        Retrieve all support tickets for the authenticated user.

        Args:
            db_session (optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response containing the user's support tickets if found, otherwise a 404 error.
        """
        tickets = SupportTicketMapper.get_tickets(user_id=session.get("user_id"), db_session=db_session)

        if not tickets:
            response_data = {"error": "No support tickets found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Support tickets retrieved", "tickets": tickets}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')

    @staticmethod
    def get_ticket(ticket_id, db_session=None):
        """
        Retrieve a specific support ticket.

        Args:
            ticket_id (int): The ID of the support ticket.
            db_session (optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response containing the support ticket details or an error message.
        """
        ticket = SupportTicketMapper.get_ticket(ticket_id=ticket_id, db_session=db_session)

        if not ticket:
            response_data = {"error": "Support ticket not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Support ticket retrieved", "ticket": ticket}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')

    @staticmethod
    def create_ticket(data, db_session=None):
        """
        Create a new support ticket.

        Args:
            data (dict): The data required to create the support ticket.
            db_session (optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response containing the newly created ticket ID or an error message.
        """
        data.update(user_id=session.get("user_id"))
        ticket_id = SupportTicketMapper.create_ticket(data=data, db_session=db_session)

        if not ticket_id:
            response_data = {"error": "Error creating support ticket"}
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype='application/json')

        response_data = {"message": "Support ticket created", "ticket_id": ticket_id}
        return Response(response=jsonify(response_data).get_data(), status=201, mimetype='application/json')

    @staticmethod
    def update_ticket(ticket_id, data, db_session=None):
        """
        Update an existing support ticket.

        Args:
            ticket_id (int): The ID of the support ticket.
            data (dict): The update data containing new ticket details.
            db_session (optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response indicating success or an error message.
        """
        updated_rows = SupportTicketMapper.update_ticket(ticket_id=ticket_id, data=data, db_session=db_session)

        if not updated_rows:
            response_data = {"error": "Support ticket not found or update failed"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Support ticket updated", "updated_rows": updated_rows}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")

    @staticmethod
    def delete_ticket(ticket_id, db_session=None):
        """
        Delete a support ticket.

        Args:
            ticket_id (int): The ID of the support ticket.
            db_session (optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response indicating success or an error message.
        """
        deleted_rows = SupportTicketMapper.delete_ticket(ticket_id=ticket_id, db_session=db_session)

        if not deleted_rows:
            response_data = {"error": "Support ticket not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Support ticket deleted", "deleted_rows": deleted_rows}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")
