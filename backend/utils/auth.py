import jwt
import functools
from flask import request, jsonify, current_app
from app.models import User

def require_auth(func):
    """Decorator to protect endpoints with JWT authentication."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header required"}), 401
        
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user = User.query.get(payload['user_id'])
            if not user:
                return jsonify({"error": "Invalid token"}), 401
            request.current_user = user
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        
        return func(*args, **kwargs)
    return wrapper
