import jwt
import bcrypt
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models import User

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json or {}
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    if not all([name, email, password]):
        return jsonify({'error': 'Name, email and password required'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user = User(name=name, email=email, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    email = data.get('email')
    password = data.get('password')
    
    if not all([email, password]):
        return jsonify({'error': 'Email and password required'}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({'token': token, 'user': user.to_dict()}), 200