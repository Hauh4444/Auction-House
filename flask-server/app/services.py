from flask import jsonify
from .data_mappers import CategoryMapper, ListingMapper

class ListingService:
    @staticmethod
    def get_all_listings(request):
        listings = ListingMapper.get_all_listings(args=request.args)
        return jsonify(listings), 200

    @staticmethod
    def get_listing_by_id(listing_id):
        listing = ListingMapper.get_listing_by_id(listing_id)
        if listing:
            return jsonify(listing), 200
        return jsonify({"error": "Listing not found"}), 404

    @staticmethod
    def create_listing(data):
        if not data.get("name"):
            return jsonify({"error": "Listing name is required"}), 400
        listing_id = ListingMapper.create_listing(data)
        return jsonify({"message": "Listing created", "listing_id": listing_id}), 201

    @staticmethod
    def update_listing(listing_id, data):
        updated_rows = ListingMapper.update_listing(listing_id, data)
        if updated_rows:
            return jsonify({"message": "Listing updated"}), 200
        return jsonify({"error": "Listing not found"}), 404

    @staticmethod
    def delete_listing(listing_id):
        deleted_rows = ListingMapper.delete_listing(listing_id)
        if deleted_rows:
            return jsonify({"message": "Listing deleted"}), 200
        return jsonify({"error": "Listing not found"}), 404
    
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