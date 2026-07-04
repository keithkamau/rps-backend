from flask import request, jsonify
from functools import wraps
import time
from collections import defaultdict

class SimpleRateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
    
    def is_rate_limited(self, key, max_requests, window_seconds):
        now = time.time()
        # Remove old requests outside the window
        self.requests[key] = [t for t in self.requests[key] if t > now - window_seconds]
        
        if len(self.requests[key]) >= max_requests:
            return True
        
        self.requests[key].append(now)
        return False

rate_limiter = SimpleRateLimiter()

def rate_limit(max_requests, window_seconds):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            key = request.remote_addr
            if rate_limiter.is_rate_limited(key, max_requests, window_seconds):
                return jsonify({'error': 'Too many requests. Slow down.'}), 429
            return f(*args, **kwargs)
        return decorated
    return decorator