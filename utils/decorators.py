"""
JWT Authentication Decorator
Provides middleware for protecting routes with JWT tokens
"""

from functools import wraps
import jwt
from flask import request, jsonify
from config import JWT_SECRET_KEY


def jwt_required(f):
    """
    Decorator to ensure that the request contains a valid, unexpired JWT in the
    Authorization: Bearer <token> header.
    
    Usage:
        @jwt_required
        def protected_route():
            officer_id = request.current_user['officer_id']
            return jsonify({"msg": "Protected data"})
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # 1. Check for Authorization Header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            # Extract the token string
            token = auth_header.split(' ')[1]

        if not token:
            return jsonify({"msg": "Authorization token is missing"}), 401

        try:
            # 2. Decode and Verify Signature & Expiration
            # This is the core verification step. If the token is invalid, tampered,
            # or expired, jwt.decode will raise an exception.
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            
            # 3. Inject officer data into the request object for use in the endpoint
            request.current_user = data
            
        except jwt.ExpiredSignatureError:
            # Token is valid but past its expiration time
            return jsonify({"msg": "Token has expired, please re-authenticate"}), 401
        except jwt.InvalidTokenError:
            # Token is invalid (signature mismatch, incorrect format, etc.)
            return jsonify({"msg": "Invalid token or signature"}), 401
        except Exception as e:
            # Catch other unexpected errors
            print(f"JWT Verification Error: {e}")
            return jsonify({"msg": "Authorization failed"}), 401

        return f(*args, **kwargs)

    return decorated
