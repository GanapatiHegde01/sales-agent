from flask import Blueprint, jsonify
from app.models import WarrantyInfo
from utils.auth import  require_auth

warranty_bp = Blueprint('warranty_bp', __name__)

# Get all warranty information
@warranty_bp.route('/', methods=['GET'])
@require_auth
def get_all_warranties():
    try:
        warranties = WarrantyInfo.query.all()
        return jsonify([w.to_dict() for w in warranties]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Get warranty details for a specific product
@warranty_bp.route('/<int:product_id>', methods=['GET'])
@require_auth
def get_warranty_by_product(product_id):
    try:
        warranty = WarrantyInfo.query.filter_by(product_id=product_id).first()
        if not warranty:
            return jsonify({"message": "No warranty found for this product"}), 404

        return jsonify(warranty.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
