"""
Security utilities
Handles authentication, authorization, and SQL security checks
"""

import re
from flask import request
from config import API_ADMIN_KEY, MAX_QUERY_LENGTH
from .responses import ResponseHelper
from .logger import log_request, get_client_ip


def require_admin_key():
    """
    Middleware to check admin key from request headers.
    
    Returns:
        Response object if unauthorized, None if authorized
    """
    admin_key = request.headers.get('x-admin-key')
    if not admin_key or admin_key != API_ADMIN_KEY:
        client_ip = get_client_ip()
        log_request(client_ip, '/admin/execute-sql', 'unauthorized', 'Missing or invalid admin key')
        return ResponseHelper.unauthorized('Unauthorized')
    return None


def is_dangerous_query(query):
    """
    Check if query contains dangerous SQL commands.
    
    Args:
        query (str): SQL query string
        
    Returns:
        tuple: (is_dangerous: bool, reason: str or None)
    """
    # Remove SQL comments
    query_cleaned = re.sub(r'/\*.*?\*/', '', query, flags=re.DOTALL)
    query_cleaned = re.sub(r'--.*?$', '', query_cleaned, flags=re.MULTILINE)
    query_cleaned = re.sub(r'#.*?$', '', query_cleaned, flags=re.MULTILINE)
    
    # Convert to uppercase for case-insensitive matching
    query_upper = query_cleaned.upper()
    
    # List of dangerous patterns
    dangerous_patterns = [
        r'\bDROP\s+DATABASE\b',
        r'\bDROP\s+TABLE\b',
        r'\bTRUNCATE\b',
        r'\bALTER\s+USER\b',
        r'\bGRANT\b',
        r'\bREVOKE\b',
        r'\bFLUSH\s+PRIVILEGES\b'
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, query_upper):
            return True, f"Dangerous pattern detected: {pattern}"
    
    return False, None


def enforce_sql_length(query_string):
    """
    Enforce SQL query length limit.
    
    Args:
        query_string (str): SQL query string
        
    Raises:
        ValueError: If query exceeds maximum length
    """
    if len(query_string) > MAX_QUERY_LENGTH:
        raise ValueError("Query too long.")
