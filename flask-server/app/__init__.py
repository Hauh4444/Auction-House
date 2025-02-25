from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_session import Session

from datetime import timedelta

from .utils import login_manager
from .database import init_db
from .auto_backup import start_scheduled_backup
from .routes import category_bp, listings_bp, review_bp, user_bp, user_profile_bp

# Initialize Flask application
app = Flask(__name__)
app.config.update(
    SECRET_KEY = "JKx6[24MJ6}1%2/'%?Q)mQua,GxQDFRtI$3K9YsIgaTPimS307GK,xfyGk(n",
    SESSION_TYPE = "filesystem",
    SESSION_USE_SIGNER = True,
    SESSION_COOKIE_NAME = "session",
    SESSION_COOKIE_HTTPONLY = True,
    SESSION_COOKIE_SAMESITE = "None",
    SESSION_COOKIE_SECURE = True,
    SESSION_PERMANENT = True,
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24),
)

# Initialize Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per hour", "20 per minute"]  # Default limit for all routes
)

# Initialize the login manager and session into the app
login_manager.init_app(app)
Session(app)

# Enable Cross-Origin Resource Sharing (CORS) for frontend communication
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "http://localhost:5173"}})

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