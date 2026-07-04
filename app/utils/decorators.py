from functools import wraps
from flask import request, jsonify
from .jwt_handler import decode_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        user_id = decode_token(token)
        if not user_id:
            return jsonify({'error': 'Token is invalid or expired'}), 401
        
        return f(user_id, *args, **kwargs)
    return decorated