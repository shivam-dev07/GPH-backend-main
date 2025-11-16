"""
Auth Routes
API endpoints for authentication operations
"""

from flask import Blueprint, request
from controllers.auth_controller import AuthController
from utils.decorators import jwt_required

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/send-otp', methods=['POST'])
def send_otp():
    """POST /api/auth/send-otp - Send OTP to phone number"""
    data = request.get_json()
    phone_number = data.get('phone_number')
    return AuthController.send_otp(phone_number)


@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    """
    POST /api/auth/verify-otp - Verify OTP and get JWT token
    
    Request body:
        {
            "phone_number": "1234567890",
            "otp_code": "123456"
        }
    
    Response:
        {
            "success": true,
            "data": {
                "message": "Authentication successful",
                "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
                "officer_id": 101,
                "staff_name": "John Doe",
                "rank": "Inspector"
            }
        }
    """
    data = request.get_json()
    phone_number = data.get('phone_number')
    otp_code = data.get('otp_code')
    
    return AuthController.verify_otp(phone_number, otp_code)


@auth_bp.route('/test-secure', methods=['GET'])
@jwt_required
def test_secure():
    """
    GET /api/auth/test-secure - Test secured endpoint
    
    This route requires a valid JWT token in the Authorization header:
    Authorization: Bearer <token>
    
    Response:
        {
            "success": true,
            "data": {
                "message": "Welcome, secured officer!",
                "officer_id": 101,
                "rank": "Inspector"
            }
        }
    """
    officer_id = request.current_user['officer_id']
    rank = request.current_user.get('rank', 'N/A')
    
    return {
        "success": True,
        "data": {
            "message": "Welcome, secured officer!",
            "officer_id": officer_id,
            "rank": rank
        }
    }, 200
