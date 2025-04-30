from gevent import monkey
monkey.patch_all()

from flask import Flask
from flask_cors import CORS

from dotenv import load_dotenv
import os, pkgutil, importlib

from .utils.limiter import limiter
from .utils.session import flask_session
from .utils.login_manager import login_manager
from .utils.mysql import mysql
from .utils.scheduler import scheduler
from .utils.socketio import socketio
from .utils.logger import setup_logger
from . import routes

logger = setup_logger(name="app_logger", log_file="logs/app.log")


def create_app():
    """
    Create and configure the Flask application instance.

    This function performs the following tasks:
    1. Loads environment variables from a `.env` file.
    2. Initializes a Flask application with a static folder.
    3. Loads configuration settings from the environment variable `FLASK_CONFIG`.
    4. Initializes Flask extensions.
    5. Dynamically imports and registers blueprints from the `routes` package.
    6. Logs any errors that occur during initialization.

    Returns:
        Flask: The configured Flask application instance.
    """
    load_dotenv()

    app = Flask(__name__, static_folder="static", static_url_path='/static')
    config_class = os.getenv("FLASK_CONFIG")
    app.config.from_object(config_class)

    # Initialize extensions with error handling
    try:
        limiter.init_app(app)
    except Exception as e:
        logger.warning(msg=f"Failed to initialize limiter in app: {e}")

    try:
        login_manager.init_app(app)
    except Exception as e:
        logger.critical(msg=f"Failed to initialize login manager in app: {e}")

    try:
        mysql.init_app(app)
    except Exception as e:
        logger.critical(msg=f"Failed to initialize MySQL in app: {e}")

    try:
        flask_session.init_app(app)
    except Exception as e:
        logger.critical(msg=f"Failed to initialize session in app: {e}")

    try:
        socketio.init_app(app, transports=["websocket"])
    except Exception as e:
        logger.critical(msg=f"Failed to initialize SocketIO in app: {e}")

    try:
        scheduler.start()
    except Exception as e:
        logger.warning(msg=f"Failed to start scheduler in app: {e}")

    try:
        CORS(app, supports_credentials=True, resources={
            r"/api/*": {"origins": os.getenv("FRONTEND_URL")},
            r"/static/*": {"origins": os.getenv("FRONTEND_URL")},
            r"/socket.io/*": {"origins": os.getenv("FRONTEND_URL")}
        })
    except Exception as e:
        logger.critical(msg=f"Failed to initialize CORS in app: {e}")

    # Register routes
    for _, module_name, _ in pkgutil.iter_modules(routes.__path__):
        try:
            module = importlib.import_module(f".{module_name}", package="app.routes")
            if hasattr(module, "bp"):
                app.register_blueprint(module.bp)
        except Exception as e:
            logger.critical(msg=f"Failed to register blueprint from module {module_name}: {e}")

    return app
