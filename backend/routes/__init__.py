from flask import Blueprint

api_bp = Blueprint("api", __name__)

from .products import products_bp
from .offers import offers_bp
from .warranty import warranty_bp
from .chat import chat_bp
from .auth import auth_bp
from .chat_history import chat_history_bp
from .admin_analytics import admin_bp

api_bp.register_blueprint(products_bp, url_prefix="/products")
api_bp.register_blueprint(offers_bp, url_prefix="/offers")
api_bp.register_blueprint(warranty_bp, url_prefix="/warranty")
api_bp.register_blueprint(chat_bp, url_prefix="/chat")
api_bp.register_blueprint(auth_bp, url_prefix="/auth")
api_bp.register_blueprint(chat_history_bp, url_prefix="/chat-history")
api_bp.register_blueprint(admin_bp, url_prefix="/admin")