from flask import jsonify, Response, session

from ..data_mappers import TicketMessageMapper, SupportTicketMapper


class TicketMessageService:
    @staticmethod
    def get_messages_by_ticket_id(ticket_id, db_session=None):
        """
        Retrieve all messages for a given ticket.
        """
        messages = TicketMessageMapper.get_messages_by_ticket_id(ticket_id=ticket_id, db_session=db_session)

        if not messages:
            response_data = {"error": "No messages found for this ticket"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Messages found", "ticket_messages": messages}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')


    @staticmethod
    def create_message(data, db_session=None):
        """
        Create a new ticket message.
        """
        message_id = TicketMessageMapper.create_message(data=data, db_session=db_session)

        if not message_id:
            response_data = {"error": "Error creating message"}
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype='application/json')

        updated_rows = SupportTicketMapper.update_ticket_timestamp(ticket_id=data.get("ticket_id"), db_session=db_session)

        if not updated_rows:
            response_data = {"error": "Error updating ticket timestamp"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Message created", "message_id": message_id}
        return Response(response=jsonify(response_data).get_data(), status=201, mimetype='application/json')


    @staticmethod
    def update_message(message_id, updates, db_session=None):
        """
        Update an existing ticket message.
        """
        updated_rows = TicketMessageMapper.update_message(message_id=message_id, updates=updates, db_session=db_session)

        if not updated_rows:
            response_data = {"error": "Message not found or no changes made"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Message updated", "updated_rows": updated_rows}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')


    @staticmethod
    def delete_message(message_id, db_session=None):
        """
        Delete a ticket message by its ID.
        """
        deleted_rows = TicketMessageMapper.delete_message(message_id=message_id, db_session=db_session)

        if not deleted_rows:
            response_data = {"error": "Message not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Message deleted", "deleted_rows": deleted_rows}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')