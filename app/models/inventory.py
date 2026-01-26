from datetime import datetime
from app import db

class Inventory(db.Model):
    __tablename__ = "inventory"

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(150), nullable=False)
    qty = db.Column(db.Integer, nullable=False, default=0)
    mrp = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "item_name": self.item_name,
            "qty": self.qty,
            "mrp": self.mrp,
            "created_at": self.created_at
        }
