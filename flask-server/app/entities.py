from dataclasses import dataclass
from datetime import datetime

@dataclass
class Category:
    def __init__(self, category_id, name, description, image_url, created_at=None, updated_at=None):
        self.category_id = category_id
        self.name = name 
        self.description = description
        self.image_url = image_url
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def to_dict(self):
        return {
            "category_id": self.category_id,
            "name": self.name,
            "description": self.description,
            "image_url": self.image_url,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }