from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_session import Session
from flask_socketio import SocketIO  # Import Flask-SocketIO

from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
import os, pkgutil, importlib

from .utils import login_manager
from .database import init_db, backup_database
from .routes import *  # Assuming routes are imported here

# Import bid routes and register them
from .bid_routes import bp as bid_routes_bp

load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Initialize Flask-SocketIO
socketio = SocketIO(app)

# Load configuration from config.py based on environment
config_class = os.getenv("FLASK_CONFIG", "app.config.DevelopmentConfig")
app.config.from_object(config_class)

# Initialize Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10000 per hour", "2000 per minute"],  # Default limit for all routes
    storage_uri="memory://",
)

# Initialize the login manager and session into the app
login_manager.init_app(app)
Session(app)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="http://localhost:5173")  # Add your frontend URL here

# Enable Cross-Origin Resource Sharing (CORS) for frontend communication
CORS(app=app, supports_credentials=True, resources={r"/api/*": {"origins": "http://localhost:5173"}})

# Initialize database
init_db()

# Register the bid_routes blueprint with the Flask app
app.register_blueprint(bid_routes_bp)

# Iterate through the modules in the routes package
for _, module_name, _ in pkgutil.iter_modules(routes.__path__):
    # Dynamically import the module
    module = importlib.import_module(name=f".{module_name}", package="app.routes")
    # Register the module blueprint
    if hasattr(module, 'bp'):
        app.register_blueprint(module.bp)

@app.route('/test', methods=['GET'])
def test():
    """Health check endpoint to verify server status.

    Returns:
        str: "Success" message if the server is running.
    """
    return 'Success'

if __name__ == '__main__':
    # Schedule background job to backup database
    scheduler = BackgroundScheduler()
    scheduler.add_job(backup_database, trigger='cron', hour=12, minute=0)  # Runs every day at Noon
    scheduler.start()

    try:
        # Run the app with SocketIO
        socketio.run(app, debug=True)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
