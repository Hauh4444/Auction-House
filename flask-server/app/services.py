from flask import jsonify
from .database import get_db
from .data_mappers import CategoryMapper

class ListingService:
    @staticmethod
    def get_all_listing(query=None, sort_by='created_at', order='desc', filters={}):
        db = get_db()
        cursor = db.cursor(dictionary=True)

        sql = "SELECT * FROM listings WHERE 1=1"
        params = []

        if query:
            sql += " AND (title LIKE %s OR description LIKE %s)"
            params.extend([f"%{query}%", f"%{query}%"])

        for column, value in filters.items():
            sql += f" AND {column} = %s"
            params.append(value)

        order = "DESC" if order == "desc" else "ASC"
        sql += f" ORDER BY {sort_by} {order}"

        cursor.execute(sql, params)
        listings = cursor.fetchall()

        return jsonify(listings), 200
    
class CategoryService:
    @staticmethod
    def get_all_categories():
        categories = CategoryMapper.get_all_categories()
        return jsonify(categories), 200

    @staticmethod
    def get_category_by_id(category_id):
        category = CategoryMapper.get_category_by_id(category_id)
        if category:
            return jsonify(category), 200
        return jsonify({"error": "Category not found"}), 404

    @staticmethod
    def create_category(data):
        if not data.get("name"):
            return jsonify({"error": "Category name is required"}), 400
        category_id = CategoryMapper.create_category(data)
        return jsonify({"message": "Category created", "category_id": category_id}), 201

    @staticmethod
    def update_category(category_id, data):
        updated_rows = CategoryMapper.update_category(category_id, data)
        if updated_rows:
            return jsonify({"message": "Category updated"}), 200
        return jsonify({"error": "Category not found"}), 404

    @staticmethod
    def delete_category(category_id):
        deleted_rows = CategoryMapper.delete_category(category_id)
        if deleted_rows:
            return jsonify({"message": "Category deleted"}), 200
        return jsonify({"error": "Category not found"}), 404