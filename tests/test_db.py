"""
Database Tests
Tests database connection and model operations
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.db import get_connection, check_health


class TestDatabase:
    """Test database connection and operations"""
    
    def test_database_connection(self):
        """Test that database connection works"""
        try:
            with get_connection() as conn:
                assert conn is not None
                assert not conn.open
        except Exception as e:
            pytest.fail(f"Database connection failed: {str(e)}")
    
    def test_health_check(self):
        """Test database health check"""
        result = check_health()
        assert result is True, "Database health check should return True"
    
    def test_query_execution(self):
        """Test basic query execution"""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 AS test_value")
                result = cursor.fetchone()
                assert result['test_value'] == 1
