from flask import Flask
from flask_cors import CORS
from flaskext.mysql import MySQL
from .routes import *

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
mysql = MySQL()
mysql.init_app(app)

#Register Blueprints
app.register_blueprint(listings_bp, url_prefix='/api/listings')
app.register_blueprint(category_bp, url_prefix='/api/category')

#Test
@app.route('/test', methods=['GET'])
def test():
    return 'Success'

if __name__ == '__main__':
    app.run(debug=True)