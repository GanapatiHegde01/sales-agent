from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat()
        }

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    specs = db.Column(db.JSON)
    stock = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": float(self.price) if self.price is not None else None,
            "description": self.description,
            "specs": self.specs,
            "stock": self.stock
        }

class Offer(db.Model):
    __tablename__ = "offers"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    discount_percentage = db.Column(db.Float, nullable=False)
    coupon_code = db.Column(db.String(50), nullable=False)
    valid_till = db.Column(db.Date, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "discount_percentage": float(self.discount_percentage),
            "coupon_code": self.coupon_code,
            "valid_till": self.valid_till.isoformat() if self.valid_till else None
        }

class WarrantyInfo(db.Model):
    __tablename__ = "warranty_info"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    warranty_period = db.Column(db.String(50), nullable=False)
    claim_process = db.Column(db.Text)

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "warranty_period": self.warranty_period,
            "claim_process": self.claim_process
        }

class ChatHistory(db.Model):
    __tablename__ = "chat_history"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    query = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "query": self.query,
            "response": self.response,
            "created_at": self.created_at.isoformat()
        }