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
    """Initialize and configure the Flask application."""
    load_dotenv()

    app = Flask(__name__)
    config_class = os.getenv("FLASK_CONFIG", "app.config.DevelopmentConfig")
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
