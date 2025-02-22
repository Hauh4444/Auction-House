from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from .database import init_db
from .auto_backup import start_scheduled_backup
from .routes import category_bp, listings_bp


# Initialize Flask application
app = Flask(__name__)

# Initialize Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="redis://localhost:6379/0",
    default_limits=["100 per hour", "20 per minute"]  # Default limit for all routes
)

# Enable Cross-Origin Resource Sharing (CORS) for frontend communication
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

# Initialize database
init_db()

# Initialize auto backup
start_scheduled_backup()

# Register Blueprints for category and listings routes
app.register_blueprint(listings_bp, url_prefix='/api/listings')
app.register_blueprint(category_bp, url_prefix='/api/categories')

# Test route to check if the server is running
@app.route('/test', methods=['GET'])
def test():
    """Health check endpoint to verify server status.

    Returns:
        str: "Success" message if the server is running.
    """
    return 'Success'

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)