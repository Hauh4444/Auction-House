from flask import Blueprint, jsonify, request, send_from_directory
from app.services.model_services import ModelService
import os

bp = Blueprint('models', __name__, url_prefix='/api/models')

MODELS_DIR = os.path.join(os.getcwd(), 'app/models/3d_models')

@bp.route('/', methods=['GET'])
def list_models():
    """
    List all 3D models with their metadata.
    """
    models = ModelService.list_models()
    return jsonify(models), 200

@bp.route('/<int:model_id>', methods=['GET'])
def get_model(model_id):
    """
    Retrieve metadata for a specific 3D model by its ID.
    """
    metadata = ModelService.get_model_metadata(model_id)
    if not metadata:
        return jsonify({"error": "Model not found"}), 404
    return jsonify(metadata), 200

@bp.route('/<int:model_id>/download', methods=['GET'])
def download_model(model_id):
    """
    Serve a 3D model file by its ID.
    """
    metadata = ModelService.get_model_metadata(model_id)
    if not metadata:
        return jsonify({"error": "Model not found"}), 404

    file_reference = metadata['file_reference']
    return send_from_directory(MODELS_DIR, file_reference)

@bp.route('/by-listing/<int:listing_id>', methods=['GET'])
def get_model_by_listing_id(listing_id):
    """
    Retrieve metadata for a 3D model by its associated listing ID.
    """
    metadata = ModelService.get_model_by_listing_id(listing_id)
    if not metadata:
        return jsonify({"error": "Model not found for the given listing ID"}), 404
    return jsonify(metadata), 200