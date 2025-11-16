"""
Auth Model
Handles authentication data access with parameterized queries
"""

from .db import get_connection
from datetime import datetime


class AuthModel:
    """Model for authentication operations"""
    
    @staticmethod
    def validate_otp(phone_number, otp_code):
        """
        Validate OTP code for a phone number.
        
        Args:
            phone_number (str): Phone number
            otp_code (str): OTP code to validate
            
        Returns:
            bool: True if OTP is valid and not expired
        """
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT otp_id, expiration_time 
                    FROM otp_codes 
                    WHERE phone_number = %s AND otp_code = %s
                """
                cursor.execute(query, (phone_number, otp_code))
                otp_record = cursor.fetchone()
                
                if not otp_record:
                    return False
                
                # Check if OTP is expired
                if otp_record['expiration_time'] < datetime.now():
                    return False
                
                return True
    
    @staticmethod
    def delete_otp(phone_number, otp_code):
        """
        Delete OTP record after successful validation.
        
        Args:
            phone_number (str): Phone number
            otp_code (str): OTP code
            
        Returns:
            bool: True if deletion was successful
        """
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    DELETE FROM otp_codes 
                    WHERE phone_number = %s AND otp_code = %s
                """
                cursor.execute(query, (phone_number, otp_code))
                conn.commit()
                return cursor.rowcount > 0
    
    @staticmethod
    def get_officer_by_phone(phone_number):
        """
        Get officer details by phone number.
        
        Args:
            phone_number (str): Phone number
            
        Returns:
            dict: Officer data or None if not found
        """
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Query the 'officer' table (matching your database structure)
                query = """
                    SELECT 
                        officer_id_number as officer_id,
                        officer_id_number as staff_id,
                        officer_name as staff_name,
                        `rank`,
                        phone_number,
                        status
                    FROM officer 
                    WHERE phone_number = %s AND is_active = 1
                """
                cursor.execute(query, (phone_number,))
                result = cursor.fetchone()
                
                return result
    
    @staticmethod
    def store_otp(phone_number, otp_code, expiration_time):
        """
        Store OTP code in database.
        
        Args:
            phone_number (str): Phone number
            otp_code (str): Generated OTP code
            expiration_time (datetime): When the OTP expires
            
        Returns:
            bool: True if storage was successful
        """
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Delete any existing OTPs for this phone number
                cursor.execute(
                    "DELETE FROM otp_codes WHERE phone_number = %s",
                    (phone_number,)
                )
                
                # Insert new OTP (matching your table structure: otp_id, phone_number, otp_code, expiration_time, attempt_count)
                query = """
                    INSERT INTO otp_codes (phone_number, otp_code, expiration_time, attempt_count)
                    VALUES (%s, %s, %s, 0)
                """
                cursor.execute(query, (phone_number, otp_code, expiration_time))
                conn.commit()
                return cursor.rowcount > 0
