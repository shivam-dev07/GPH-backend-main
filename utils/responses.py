"""
Response utilities
Centralized JSON response helpers for consistent API responses
"""

from flask import jsonify


class ResponseHelper:
    """Centralized JSON response helpers for consistent API responses"""
    
    @staticmethod
    def success_select(rows):
        """
        Success response for SELECT queries.
        
        Args:
            rows (list): Query result rows
            
        Returns:
            tuple: (response, status_code)
        """
        return jsonify({
            'success': True,
            'type': 'select',
            'rows': rows
        }), 200
    
    @staticmethod
    def success_write(rows_affected):
        """
        Success response for INSERT/UPDATE/DELETE queries.
        
        Args:
            rows_affected (int): Number of rows affected
            
        Returns:
            tuple: (response, status_code)
        """
        return jsonify({
            'success': True,
            'type': 'write',
            'rows_affected': rows_affected
        }), 200
    
    @staticmethod
    def success_data(data):
        """
        Generic success response with data.
        
        Args:
            data: Response data (dict, list, etc.)
            
        Returns:
            tuple: (response, status_code)
        """
        return jsonify({
            'success': True,
            'data': data
        }), 200
    
    @staticmethod
    def error(message, status_code=400):
        """
        Error response.
        
        Args:
            message (str): Error message
            status_code (int): HTTP status code
            
        Returns:
            tuple: (response, status_code)
        """
        return jsonify({
            'success': False,
            'error': message
        }), status_code
    
    @staticmethod
    def unauthorized(message='Unauthorized'):
        """
        Unauthorized response.
        
        Args:
            message (str): Error message
            
        Returns:
            tuple: (response, status_code)
        """
        return jsonify({
            'success': False,
            'error': message
        }), 401
    
    @staticmethod
    def blocked(message='Dangerous query blocked.'):
        """
        Blocked query response.
        
        Args:
            message (str): Block reason
            
        Returns:
            tuple: (response, status_code)
        """
        return jsonify({
            'success': False,
            'error': message
        }), 400
    
    @staticmethod
    def internal_error():
        """
        Internal server error response (no stack trace).
        
        Returns:
            tuple: (response, status_code)
        """
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


# Convenience functions for controllers
def success_response(data, status_code=200):
    """
    Generic success response helper.
    
    Args:
        data: Response data
        status_code (int): HTTP status code
        
    Returns:
        tuple: (response, status_code)
    """
    return jsonify({
        'success': True,
        'data': data
    }), status_code


def error_response(message, status_code=400):
    """
    Generic error response helper.
    
    Args:
        message (str): Error message
        status_code (int): HTTP status code
        
    Returns:
        tuple: (response, status_code)
    """
    return jsonify({
        'success': False,
        'error': message
    }), status_code
