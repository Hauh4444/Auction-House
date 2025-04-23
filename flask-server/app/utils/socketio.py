from flask_socketio import SocketIO

from dotenv import load_dotenv
import os

from .logger import setup_logger

load_dotenv()

logger = setup_logger(name="app_logger", log_file="logs/app.log")


try:
    # Initialize SocketIO
    socketio = SocketIO(cors_allowed_origins=os.getenv("FRONTEND_URL"))
except Exception as e:
    # Log any errors during SocketIO initialization
    logger.critical(msg=f"SocketIO initialization error: {e}")