from flask_login import current_user
from flask_socketio import disconnect

from app import create_app

from .utils.socketio import socketio
from .utils.logger import setup_logger

app = create_app()

logger = setup_logger(name="app_logger", log_file="logs/app.log")


if __name__ == "__main__":
    try:
        socketio.run(app, host="127.0.0.1", port=5000, debug=True)
    except Exception as e:
        logger.info(msg=f"Failed to start the SocketIO server: {e}")


@app.errorhandler(429)
def ratelimit_handler(e):
    # Log the rate limit exceeded error
    logger.warning(msg=f"Rate limit exceeded: {e.description}")
    return {"error": "Rate limit exceeded"}, 429