import os
from flask import jsonify
from app.database.connection import get_db

MODELS_DIR = os.path.join(os.getcwd(), 'app/models/3d_models')

class ModelService:
    @staticmethod
    def get_model_metadata(model_id):
        """
        Retrieve metadata for a specific 3D model by its ID.

        Args:
            model_id (int): The ID of the model.

        Returns:
            dict: Metadata for the model, or None if not found.
        """
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM models WHERE id = %s", (model_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if not result:
            return None

        metadata = {
            "id": result[0],
            "name": result[1],
            "file_path": result[2],
            "created_at": result[3]
        }
        return metadata

    @staticmethod
    def list_models():
        """
        List all 3D models with their metadata.

        Returns:
            list: A list of metadata for all models.
        """
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM models")
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        models = [
            {
                "id": row[0],
                "name": row[1],
                "file_path": row[2],
                "created_at": row[3]
            }
            for row in results
        ]
        return models

    @staticmethod
    def add_model(name, file_path):
        """
        Add a new 3D model to the database.

        Args:
            name (str): The name of the model.
            file_path (str): The file path of the model.

        Returns:
            int: The ID of the newly created model.
        """
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO models (name, file_path) VALUES (%s, %s)",
            (name, file_path)
        )
        conn.commit()
        model_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return model_id

    @staticmethod
    def delete_model(model_id):
        """
        Delete a 3D model by its ID.

        Args:
            model_id (int): The ID of the model to delete.

        Returns:
            bool: True if the model was deleted, False otherwise.
        """
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM models WHERE id = %s", (model_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return deleted