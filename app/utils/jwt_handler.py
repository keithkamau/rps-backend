import jwt
from datetime import datetime, timedelta
from flask import current_app

def create_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

def decode_token(token):
    try:
        payload = jwt.decode(
            token, 
            current_app.config['JWT_SECRET_KEY'], 
            algorithms=['HS256']
        )
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None