from flask import Flask
from flask_cors import CORS
from flaskext.mysql import MySQL

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
mysql = MySQL()
mysql.init_app(app)

@app.route('/test', methods=['GET'])
def test():
    return 'Success'

if __name__ == '__main__':
    app.run(debug=True)