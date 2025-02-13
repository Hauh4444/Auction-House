from flask import Flask
from flask_cors import CORS

from .database import init_db
from .routes.category import category_bp
from .routes.listings import listings_bp

# Initialize Flask application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for frontend communication
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

# Initialize database
init_db()

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
