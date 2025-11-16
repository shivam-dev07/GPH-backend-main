"""
Admin Tests
Tests admin endpoints and SQL execution
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from config import API_ADMIN_KEY


@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestAdminEndpoints:
    """Test admin endpoints"""
    
    def test_admin_sql_unauthorized(self, client):
        """Test admin SQL without auth header"""
        response = client.post('/admin/execute-sql', json={'query': 'SELECT 1'})
        assert response.status_code == 401
        assert response.json['success'] is False
    
    def test_admin_sql_wrong_key(self, client):
        """Test admin SQL with wrong key"""
        response = client.post(
            '/admin/execute-sql',
            json={'query': 'SELECT 1'},
            headers={'x-admin-key': 'wrong_key'}
        )
        assert response.status_code == 401
    
    def test_admin_sql_missing_query(self, client):
        """Test admin SQL without query parameter"""
        response = client.post(
            '/admin/execute-sql',
            json={},
            headers={'x-admin-key': API_ADMIN_KEY}
        )
        assert response.status_code == 400
        assert 'query' in response.json['error'].lower()
    
    def test_admin_sql_valid_select(self, client):
        """Test admin SQL with valid SELECT query"""
        response = client.post(
            '/admin/execute-sql',
            json={'query': 'SELECT 1 AS test_value'},
            headers={'x-admin-key': API_ADMIN_KEY}
        )
        assert response.status_code == 200
        assert response.json['success'] is True
        assert response.json['type'] == 'select'
        assert len(response.json['rows']) > 0
    
    def test_admin_sql_dangerous_drop_table(self, client):
        """Test that DROP TABLE is blocked"""
        response = client.post(
            '/admin/execute-sql',
            json={'query': 'DROP TABLE users'},
            headers={'x-admin-key': API_ADMIN_KEY}
        )
        assert response.status_code == 400
        assert 'dangerous' in response.json['error'].lower()
    
    def test_admin_sql_dangerous_truncate(self, client):
        """Test that TRUNCATE is blocked"""
        response = client.post(
            '/admin/execute-sql',
            json={'query': 'TRUNCATE TABLE users'},
            headers={'x-admin-key': API_ADMIN_KEY}
        )
        assert response.status_code == 400
        assert 'dangerous' in response.json['error'].lower()
    
    def test_admin_sql_query_too_long(self, client):
        """Test query length limit"""
        long_query = 'SELECT ' + ', '.join([f"'{i}' AS col{i}" for i in range(2000)])
        response = client.post(
            '/admin/execute-sql',
            json={'query': long_query},
            headers={'x-admin-key': API_ADMIN_KEY}
        )
        assert response.status_code == 400
        assert 'too long' in response.json['error'].lower()
