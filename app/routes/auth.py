from flask import Blueprint, request, jsonify
from app import db, limiter
from app.models.user import User
from app.models.statistics import UserStatistics
from app.utils.jwt_handler import create_token
from app.utils.decorators import token_required
import re

auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain an uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain a lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain a number"
    return True, ""

@auth_bp.route('/signup', methods=['POST'])
@limiter.limit("5 per minute")
def signup():
    data = request.get_json()
    
    # Validation
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Username, email, and password are required'}), 400
    
    username = data['username'].strip()
    email = data['email'].strip().lower()
    password = data['password']
    
    if len(username) < 3 or len(username) > 50:
        return jsonify({'error': 'Username must be between 3 and 50 characters'}), 400
    
    if not validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400
    
    valid, msg = validate_password(password)
    if not valid:
        return jsonify({'error': msg}), 400
    
    # Check existing user
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already taken'}), 409
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    # Create user
    user = User(username=username, email=email)
    user.set_password(password)
    
    # Create statistics
    stats = UserStatistics(user=user)
    
    db.session.add(user)
    db.session.add(stats)
    db.session.commit()
    
    token = create_token(user.id)
    
    return jsonify({
        'message': 'User created successfully',
        'user': user.to_dict(),
        'token': token
    }), 201

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400
    
    username = data['username'].strip()
    password = data['password']
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Account is deactivated'}), 403
    
    token = create_token(user.id)
    
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict(),
        'token': token
    }), 200

@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'user': user.to_dict()}), 200