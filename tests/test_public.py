"""
Public API Tests
Tests public endpoints
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app


@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestPublicEndpoints:
    """Test public API endpoints"""
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        assert response.json['success'] is True
        assert response.json['data']['status'] == 'healthy'
    
    def test_get_officers(self, client):
        """Test get all officers endpoint"""
        response = client.get('/officers')
        assert response.status_code == 200
        assert response.json['success'] is True
        assert 'data' in response.json
        assert isinstance(response.json['data'], list)
    
    def test_get_officer_invalid_id(self, client):
        """Test get officer with invalid ID"""
        response = client.get('/officers/ ')
        assert response.status_code == 400
        assert response.json['success'] is False
    
    def test_404_endpoint(self, client):
        """Test non-existent endpoint returns 404"""
        response = client.get('/nonexistent')
        assert response.status_code == 404
        assert response.json['success'] is False
        assert 'not found' in response.json['error'].lower()
