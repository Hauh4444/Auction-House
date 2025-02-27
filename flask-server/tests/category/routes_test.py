import pytest
from flask import Flask
from app.routes import category_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(category_bp, url_prefix='/api/categories')
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()
