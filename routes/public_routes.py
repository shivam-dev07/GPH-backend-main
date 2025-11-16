"""
Public Routes
Defines public API endpoints
"""

from flask import Blueprint
from controllers.public_controller import PublicController

public_bp = Blueprint('public', __name__)


@public_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    
    Request:
        GET /health
    
    Response:
        {
            "success": true,
            "data": {
                "status": "healthy",
                "database": "connected",
                "timestamp": "2025-11-15T04:48:00.000000Z"
            }
        }
    """
    return PublicController.health_check()


@public_bp.route('/officers', methods=['GET'])
def get_officers():
    """
    Get all officers endpoint.
    
    Request:
        GET /officers
    
    Response:
        {
            "success": true,
            "data": [
                {
                    "id": "GP02650",
                    "staff_id": "GP02650",
                    "staff_name": "John Doe",
                    "staff_designation": "Police Constable",
                    "staff_nature_of_work": "Patrol Duty",
                    "status": "active",
                    "created_at": "...",
                    "updated_at": "..."
                },
                ...
            ]
        }
    """
    return PublicController.get_all_officers()


@public_bp.route('/officers/<string:officer_id>', methods=['GET'])
def get_officer(officer_id):
    """
    Get officer by ID endpoint.
    
    Request:
        GET /officers/<officer_id>
    
    Response:
        {
            "success": true,
            "data": {
                "id": "GP02650",
                "staff_id": "GP02650",
                "staff_name": "John Doe",
                "staff_designation": "Police Constable",
                "staff_nature_of_work": "Patrol Duty",
                "status": "active",
                "created_at": "...",
                "updated_at": "..."
            }
        }
    """
    return PublicController.get_officer_by_id(officer_id)
