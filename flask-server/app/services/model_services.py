import os
from app.database.connection import get_db
from app.entities.model import Model

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
        cursor.execute("SELECT * FROM models WHERE model_id = %s", (model_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if not result:
            return None

        model = Model(
            model_id=result[0],
            name=result[1],
            file_reference=result[2],
            file_size=result[3],
            listing_id=result[4],
            created_at=result[5],
            updated_at=result[6]
        )
        return model.to_dict()

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
            Model(
                model_id=row[0],
                name=row[1],
                file_reference=row[2],
                file_size=row[3],
                listing_id=row[4],
                created_at=row[5],
                updated_at=row[6]
            ).to_dict()
            for row in results
        ]
        return models

    @staticmethod
    def add_model(name, file_reference, file_size, listing_id):
        """
        Add a new 3D model to the database.

        Args:
            name (str): The name of the model.
            file_reference (str): The file path or reference to the model.
            file_size (float): The size of the model file in megabytes.
            listing_id (int): The ID of the associated listing.

        Returns:
            int: The ID of the newly created model.
        """
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO models (name, file_reference, file_size, listing_id) VALUES (%s, %s, %s, %s)",
            (name, file_reference, file_size, listing_id)
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
        cursor.execute("DELETE FROM models WHERE model_id = %s", (model_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return deleted

    @staticmethod
    def get_model_by_listing_id(listing_id):
        """
        Retrieve the model ID and metadata for a specific listing ID.

        Args:
            listing_id (int): The ID of the listing.

        Returns:
            dict: Metadata for the model, or None if not found.
        """
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM models WHERE listing_id = %s", (listing_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if not result:
            return None

        model = {
            "model_id": result[0],
            "name": result[1],
            "file_reference": result[2],
            "file_size": result[3],
            "listing_id": result[4],
            "created_at": result[5],
            "updated_at": result[6]
        }
        return model