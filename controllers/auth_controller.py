"""
Auth Controller
Handles authentication business logic including OTP verification and JWT generation
"""

import jwt
from datetime import datetime, timedelta, timezone
from models.auth_model import AuthModel
from config import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES
from utils.logger import log_info, log_error
from utils.responses import success_response, error_response


class AuthController:
    """Controller for authentication operations"""
    
    @staticmethod
    def verify_otp(phone_number, otp_code):
        """
        Verify OTP and generate JWT token.
        
        Args:
            phone_number (str): Phone number
            otp_code (str): OTP code to verify
            
        Returns:
            tuple: (response_dict, status_code)
        """
        try:
            if not phone_number or not otp_code:
                return error_response("Missing phone number or OTP code", 400)
            
            log_info(f"OTP verification attempt for phone: {phone_number}")
            
            # Validate OTP
            is_valid = AuthModel.validate_otp(phone_number, otp_code)
            
            if not is_valid:
                log_info(f"Invalid or expired OTP for phone: {phone_number}")
                return error_response("Invalid or expired OTP", 401)
            
            # Get officer data
            officer_data = AuthModel.get_officer_by_phone(phone_number)
            
            if not officer_data:
                log_error(f"Officer not found for phone: {phone_number}")
                return error_response("Officer not found", 404)
            
            # Delete used OTP
            AuthModel.delete_otp(phone_number, otp_code)
            
            # Generate JWT token
            expire_time = datetime.now(timezone.utc) + JWT_ACCESS_TOKEN_EXPIRES
            
            payload = {
                'officer_id': officer_data['officer_id'],
                'staff_id': officer_data['staff_id'],
                'rank': officer_data['rank'],
                'phone': officer_data['phone_number'],
                'exp': expire_time
            }
            
            token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
            
            log_info(f"Authentication successful for officer: {officer_data['officer_id']}")
            
            return success_response({
                "message": "Authentication successful",
                "token": token,
                "officer_id": officer_data['officer_id'],
                "staff_name": officer_data['staff_name'],
                "rank": officer_data['rank']
            })
            
        except Exception as e:
            log_error(f"Error during OTP verification: {str(e)}")
            return error_response("Internal server error during authentication", 500)
    
    @staticmethod
    def send_otp(phone_number):
        """
        Generate and send OTP to phone number.
        
        Args:
            phone_number (str): Phone number to send OTP to
            
        Returns:
            tuple: (response_dict, status_code)
        """
        try:
            if not phone_number:
                return error_response("Missing phone number", 400)
            
            log_info(f"OTP request for phone: {phone_number}")
            
            # Check if officer exists
            officer_data = AuthModel.get_officer_by_phone(phone_number)
            
            if not officer_data:
                log_info(f"Officer not found for phone: {phone_number}")
                return error_response("Officer not found", 404)
            
            # Generate OTP (6 digits)
            import random
            otp_code = str(random.randint(100000, 999999))
            
            # Set expiration time (5 minutes from now)
            expiration_time = datetime.now() + timedelta(minutes=5)
            
            # Store OTP in database
            AuthModel.store_otp(phone_number, otp_code, expiration_time)
            
            # TODO: Send OTP via SMS service (e.g., Twilio, AWS SNS, etc.)
            # For now, we'll just log it (REMOVE IN PRODUCTION)
            log_info(f"OTP generated for {phone_number}: {otp_code}")
            
            return success_response({
                "message": "OTP sent successfully",
                "otp": otp_code  # TODO: REMOVE THIS IN PRODUCTION
            })
            
        except Exception as e:
            log_error(f"Error sending OTP: {str(e)}")
            return error_response("Failed to send OTP", 500)
