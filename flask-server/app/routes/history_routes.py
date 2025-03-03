from flask import Blueprint, request
from flask_login import login_required

from ..services import HistoryService

# Blueprint for history-related routes
bp = Blueprint('history_bp', __name__, url_prefix="/api/user/<int:id>")

# TODO: GET /api/user/<int:id>/history          for full user history
#       GET /api/user/<int:id>/orders           for user's previous orders
#       Others will be needed but these are simply a couple examples to show what the routes will look like
#       Routes should all be preceded with the @login_required decorator

