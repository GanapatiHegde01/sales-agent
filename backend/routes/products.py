from flask import Blueprint, jsonify, request
from app.models import Product
from app import db
from utils.auth import require_auth


products_bp = Blueprint("products_bp", __name__)

@products_bp.route("/", methods=["GET"])
@require_auth
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    products = Product.query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        "products": [p.to_dict() for p in products.items],
        "total": products.total,
        "pages": products.pages,
        "current_page": page,
        "per_page": per_page
    })

@products_bp.route("/<int:product_id>", methods=["GET"])
@require_auth
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())

@products_bp.route("/", methods=["POST"])
@require_auth
def add_product():
    data = request.json or {}
    product = Product(
        name=data.get("name"),
        category=data.get("category"),
        price=data.get("price", 0.0),
        description=data.get("description"),
        specs=data.get("specs") or {},
        stock=data.get("stock", 0)
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201

@products_bp.route("/load-data", methods=["POST"])
def load_sample_data():
    """Load sample data from CSV files"""
    try:
        from utils.db_utils import load_csv_to_db
        import os
        
        products_csv = os.getenv("PRODUCTS_CSV", "datasets/products.csv")
        offers_csv = os.getenv("OFFERS_CSV", "datasets/offers.csv")
        warranty_csv = os.getenv("WARRANTY_CSV", "datasets/warranty_info.csv")
        
        if os.path.exists(products_csv):
            load_csv_to_db(products_csv, offers_csv, warranty_csv)
            return jsonify({"message": "Data loaded successfully"}), 200
        else:
            return jsonify({"error": f"CSV file not found: {products_csv}"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500