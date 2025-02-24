from flask import Flask
from flask_cors import CORS

from .database import init_db
from .auto_backup import start_scheduled_backup
from .routes import category_bp, listings_bp, review_bp, user_bp, user_profile_bp


# Initialize Flask application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for frontend communication
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

# Initialize database
init_db()

# Initialize auto backup
start_scheduled_backup()

# Register Blueprints for routes
app.register_blueprint(listings_bp, url_prefix='/api/listings')
app.register_blueprint(category_bp, url_prefix='/api/categories')
app.register_blueprint(review_bp, url_prefix='/api/reviews')
app.register_blueprint(user_bp, url_prefix='/api/user')
app.register_blueprint(user_profile_bp, url_prefix='/api/profile')

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