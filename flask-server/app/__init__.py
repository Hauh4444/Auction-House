from flask import Flask
from flask_cors import CORS

from .database import init_db
from .routes.category import category_bp
from .routes.listings import listings_bp

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
init_db()

# Register Blueprints
app.register_blueprint(listings_bp, url_prefix='/api/listings')
app.register_blueprint(category_bp, url_prefix='/api/categories')


# Test
@app.route('/test', methods=['GET'])
def test():
    return 'Success'


if __name__ == '__main__':
    app.run(debug=True)
