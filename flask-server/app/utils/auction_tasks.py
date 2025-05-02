from celery import shared_task
from .socketio import socketio


@shared_task
def end_auction_task(listing_id):
    socketio.emit("auction_ended", {"listing_id": listing_id})
