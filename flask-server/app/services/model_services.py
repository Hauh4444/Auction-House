from flask import jsonify, Response, send_from_directory

from dotenv import load_dotenv
import os

from ..data_mappers import ModelMapper
from ..utils.logger import setup_logger

load_dotenv()

logger = setup_logger(name="model_logger", log_file="logs/model.log")


class ModelService:
    @staticmethod
    def get_all_models(db_session=None):
        """
        List all 3D models with their metadata.

        Args:
            db_session: Optional database session to be used in tests.

        Returns:
            Response: A JSON response containing the list of models.
                Returns status code 404 if no models are found.
        """
        models = ModelMapper.get_all_models(db_session=db_session)
        if not models:
            response_data = {"error": "No models found"}
            logger.error(msg=f"No models found")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Models found", "models": models}
        logger.info(msg=f"Models found: {[model.get('file_reference') for model in models]}")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def get_model_by_listing_id(listing_id: int, db_session=None):
        """
        Retrieve the model ID and metadata for a specific listing ID.

        Args:
            listing_id (int): The ID of the listing.
            db_session: Optional database session to be used in tests.

        Returns:
            Response: A JSON response containing the model data if found.
                Returns status code 404 if the model is not found.
        """
        model = ModelMapper.get_model_by_listing_id(listing_id=listing_id, db_session=db_session)
        if not model:
            response_data = {"error": "Model not found"}
            logger.error(msg=f"Model not found for listing: {listing_id}")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        model.update(file_reference=f"{os.getenv("BACKEND_MODEL_URL")}/{model.get("file_reference")}")

        response_data = {"message": "Model found", "model": model}
        logger.info(msg=f"Model: {model.get('file_reference')} found for listing: {listing_id}")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def get_model_by_model_id(model_id: int, db_session=None):
        """
        Serve a 3D model file by its ID.

        Args:
            model_id (int): The ID of the model.
            db_session: Optional database session to be used in tests.

        Returns:
            Response: A JSON response containing the model file if found.
                Returns status code 404 if the model is not found.
        """
        model = ModelMapper.get_model_by_model_id(model_id=model_id, db_session=db_session)
        if not model:
            response_data = {"error": "Model not found"}
            logger.error(msg=f"Model: {model_id} not found")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        model.update(file_reference=f"{os.getenv("BACKEND_URL")}/api/models/{model.get("file_reference")}")

        response_data = {"message": "Model found", "model": model}
        logger.info(msg=f"Model: {model_id} found")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def download_model(model_id: int, db_session=None):
        """
        Serve a 3D model file by its ID.

        Args:
            model_id (int): The ID of the model.
            db_session: Optional database session to be used in tests.

        Returns:
            Response: A JSON response containing the model file if found.
                Returns status code 404 if the model is not found.
        """
        model = ModelMapper.get_model_by_model_id(model_id=model_id, db_session=db_session)
        if not model:
            response_data = {"error": "Model not found"}
            logger.error(msg=f"Model: {model_id} not found")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        models_directory = os.path.join(os.getcwd(), 'models/')
        model_file = send_from_directory(models_directory, model.get("file_reference"))
        if not model_file:
            response_data = {"error": "Model not found"}
            logger.error(msg=f"Model: {model_file} not found")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Model found", "model": model_file}
        logger.info(msg=f"Model: {model_file} found")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def create_model(data: dict, db_session=None):
        """
        Add a new 3D model to the database.

        Args:
            data (dict): A dictionary containing the model details (e.g., name).
            db_session: Optional database session to be used in tests.

        Returns:
            Response: A JSON response with the success message and newly created model ID.
                Returns status code 409 if there was an error creating the model.
        """
        model_id = ModelMapper.create_model(data=data, db_session=db_session)
        if not model_id:
            response_data = {"error": "Error creating model"}
            logger.error(msg=f"Failed creating model with data: {', '.join(f'{k}={v!r}' for k, v in data.items())}")
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

        response_data = {"message": "Model created", "model_id": model_id}
        logger.info(msg=f"Model: {model_id} created successfully with data: {', '.join(f'{k}={v!r}' for k, v in data.items())}")
        return Response(response=jsonify(response_data).get_data(), status=201, mimetype="application/json")


    @staticmethod
    def delete_model(model_id: int, db_session=None):
        """
        Delete a 3D model by its ID.

        Args:
            model_id (int): The ID of the model to delete.
            db_session: Optional database session to be used in tests.

        Returns:
            Response: A JSON response with a success message if the model was deleted.
                Returns status code 404 if the model was not found.
        """
        deleted_rows = ModelMapper.delete_model(model_id=model_id, db_session=db_session)
        if not deleted_rows:
            response_data = {"error": "Model not found"}
            logger.error(msg=f"Model: {model_id} not found")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Model deleted", "deleted_rows": deleted_rows}
        logger.info(msg=f"Model: {model_id} deleted successfully")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")