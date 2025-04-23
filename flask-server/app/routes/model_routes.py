from flask import Blueprint

from ..services import ModelService

bp = Blueprint('models', __name__, url_prefix='/api/models')


# GET /api/models/
@bp.route('/', methods=['GET'])
def get_all_models():
    """
    List all 3D models with their metadata.
    """
    return ModelService.get_all_models()


# GET /api/models/listing/{id}/
@bp.route('/listing/<int:listing_id>/', methods=['GET'])
def get_model_by_listing_id(listing_id):
    """
    Retrieve metadata for a 3D model by its associated listing ID.
    """
    return ModelService.get_model_by_listing_id(listing_id=listing_id)


# GET /api/models/{id}/
@bp.route('/<int:model_id>/', methods=['GET'])
def get_model_by_model_id(model_id):
    """
    Serve a 3D model file by its ID.
    """
    return ModelService.get_model_by_model_id(model_id=model_id)


# GET /api/models/download/{id}/
@bp.route('/download/<int:model_id>/', methods=['GET'])
def download_model(model_id):
    """
    Serve a 3D model file by its ID.
    """
    return ModelService.get_model_by_model_id(model_id=model_id)