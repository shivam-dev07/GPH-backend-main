"""
Officer Routes
Maps officer HTTP endpoints to controller methods
"""

from flask import Blueprint, request
from controllers.officer_controller import OfficerController

officer_bp = Blueprint('officer', __name__, url_prefix='/api')

@officer_bp.route('/officers', methods=['GET'])
def get_all_officers():
    """GET /api/officers - Get all officers"""
    return OfficerController.get_all_officers()

@officer_bp.route('/officers/<officer_id>', methods=['GET'])
def get_officer(officer_id):
    """GET /api/officers/:id - Get single officer"""
    return OfficerController.get_officer(officer_id)

@officer_bp.route('/officers', methods=['POST'])
def create_officer():
    """POST /api/officers - Create a new officer"""
    data = request.get_json()
    return OfficerController.create_officer(data)

@officer_bp.route('/officers/<officer_id>', methods=['PUT'])
def update_officer(officer_id):
    """PUT /api/officers/:id - Update an officer"""
    data = request.get_json()
    return OfficerController.update_officer(officer_id, data)

@officer_bp.route('/officers/<officer_id>', methods=['DELETE'])
def delete_officer(officer_id):
    """DELETE /api/officers/:id - Delete an officer"""
    return OfficerController.delete_officer(officer_id)