from flask import Blueprint, jsonify, request
from app.models import Offer
from app import db
from datetime import datetime

from utils.auth import require_auth

offers_bp = Blueprint("offers_bp", __name__)

@offers_bp.route("/", methods=["GET"])
@require_auth
def get_offers():
    offers = Offer.query.all()
    return jsonify([o.to_dict() for o in offers])

@offers_bp.route("/<int:offer_id>", methods=["GET"])
@require_auth
def get_offer(offer_id):
    offer = Offer.query.get_or_404(offer_id)
    return jsonify(offer.to_dict())

@offers_bp.route("/", methods=["POST"])
@require_auth
def add_offer():
    data = request.json or {}
    valid_till = data.get("valid_till")
    # Accept ISO date string or None
    offer = Offer(
        product_id=data.get("product_id"),
        discount_percentage=data.get("discount_percentage", 0),
        coupon_code=data.get("coupon_code", ""),
        valid_till=valid_till
    )
    db.session.add(offer)
    db.session.commit()
    return jsonify(offer.to_dict()), 201