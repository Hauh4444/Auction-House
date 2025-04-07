from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os, pkgutil, importlib

from .utils.limiter import limiter
from .utils.session import session
from .utils.login_manager import login_manager
from .utils.mysql import mysql
from .utils.scheduler import scheduler
from . import routes


def create_app():
    """
    Initialize and configure the Flask application with required extensions and blueprints.

    This function performs the following tasks:
    1. Loads environment variables from a `.env` file using `load_dotenv()`.
    2. Loads the configuration class specified by the environment variable `FLASK_CONFIG`.
    3. Initializes Flask extensions:
        - Limiter: Manages rate limiting for API routes.
        - Login Manager: Handles user authentication and session management.
        - MySQL: Sets up the MySQL connection.
        - Session: Manages user sessions.
        - Scheduler: Starts the background job scheduler for periodic tasks.
        - CORS: Configures Cross-Origin Resource Sharing (CORS) to allow the frontend to interact with the backend from different origins.
    4. Registers API blueprints dynamically by iterating through modules in the `routes` folder.
    5. Returns the Flask application instance with all configurations and routes.

    Returns:
        Flask: The configured Flask application instance.
    """
    load_dotenv()

    app = Flask(__name__)
    config_class = os.getenv("FLASK_CONFIG")
    app.config.from_object(config_class)

    # Initialize extensions
    limiter.init_app(app)
    login_manager.init_app(app)
    mysql.init_app(app)
    session.init_app(app)
    scheduler.start()
    CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "http://localhost:5173"}})

    # Register routes
    for _, module_name, _ in pkgutil.iter_modules(routes.__path__):
        module = importlib.import_module(f".{module_name}", package="app.routes")
        if hasattr(module, "bp"):
            app.register_blueprint(module.bp)

    return app
