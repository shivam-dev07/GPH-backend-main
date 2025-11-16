"""
Admin Model
Handles admin SQL execution with security checks
"""

from .db import get_connection
from utils.security import is_dangerous_query, enforce_sql_length
from config import ALLOW_WRITE_QUERIES
from utils.logger import logger


class AdminModel:
    """Model for admin operations (raw SQL execution)"""
    
    @staticmethod
    def execute_raw_query(query_string):
        """
        Execute raw SQL query (admin-only).
        Returns dict with success, type, and rows/rows_affected.
        Raises exceptions on errors.
        
        Args:
            query_string (str): SQL query to execute
            
        Returns:
            dict: {
                'success': True,
                'type': 'select' | 'write',
                'rows': [...] | 'rows_affected': int
            }
            
        Raises:
            ValueError: If query is too long or dangerous
            Exception: For database errors
        """
        # Enforce query length limit
        enforce_sql_length(query_string)
        
        # Check for dangerous queries
        is_dangerous, reason = is_dangerous_query(query_string)
        if is_dangerous:
            raise ValueError("Dangerous query blocked.")
        
        # Execute query
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query_string)
                
                # Determine query type
                query_upper = query_string.strip().upper()
                
                if query_upper.startswith('SELECT') or query_upper.startswith('SHOW') or query_upper.startswith('DESCRIBE'):
                    # SELECT query
                    rows = cursor.fetchall()
                    return {
                        'success': True,
                        'type': 'select',
                        'rows': rows
                    }
                else:
                    # INSERT/UPDATE/DELETE query
                    rows_affected = cursor.rowcount
                    conn.commit()
                    return {
                        'success': True,
                        'type': 'write',
                        'rows_affected': rows_affected
                    }
