from pymysql import cursors

from ..database import get_db
from ..entities import Model


class ModelMapper:
    @staticmethod
    def get_all_models(db_session=None):
        """
        Retrieve all models.

        Args:
            db_session: Optional database session to be used in tests.

        Returns:
            dict: Model details if found, otherwise None.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM models")
        models = cursor.fetchall()
        return [Model(**model).to_dict() for model in models]


    @staticmethod
    def get_model_by_listing_id(listing_id: int, db_session=None):
        """
        Retrieve all models.

        Args:
            listing_id (int): The ID of the listing.
            db_session: Optional database session to be used in tests.

        Returns:
            dict: Model details if found, otherwise None.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM models WHERE listing_id = %s", (listing_id,))
        model = cursor.fetchone()
        return Model(**model).to_dict() if model else None


    @staticmethod
    def get_model_by_model_id(model_id: int, db_session=None):
        """
        Retrieve all models.

        Args:
            model_id (int): The ID of the model.
            db_session: Optional database session to be used in tests.

        Returns:
            dict: Model details if found, otherwise None.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM models WHERE model_id = %s", (model_id,))
        model = cursor.fetchone()
        return Model(**model).to_dict() if model else None