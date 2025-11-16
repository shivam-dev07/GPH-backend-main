"""
Duty Location Routes
API endpoints for saved duty location operations
"""

from flask import Blueprint, request
from controllers.duty_location_controller import DutyLocationController

duty_location_bp = Blueprint('duty_location', __name__, url_prefix='/api/duty-locations')


@duty_location_bp.route('', methods=['GET'])
def get_all_duty_locations():
    """GET /api/duty-locations - Get all saved duty locations"""
    return DutyLocationController.get_all_duty_locations()


@duty_location_bp.route('/<location_id>', methods=['GET'])
def get_duty_location(location_id):
    """GET /api/duty-locations/:id - Get duty location by ID"""
    return DutyLocationController.get_duty_location(location_id)


@duty_location_bp.route('', methods=['POST'])
def create_duty_location():
    """POST /api/duty-locations - Create new duty location"""
    location_data = request.get_json()
    return DutyLocationController.create_duty_location(location_data)


@duty_location_bp.route('/<location_id>', methods=['PUT', 'PATCH'])
def update_duty_location(location_id):
    """PUT/PATCH /api/duty-locations/:id - Update duty location"""
    updates = request.get_json()
    return DutyLocationController.update_duty_location(location_id, updates)


@duty_location_bp.route('/<location_id>', methods=['DELETE'])
def delete_duty_location(location_id):
    """DELETE /api/duty-locations/:id - Delete duty location"""
    return DutyLocationController.delete_duty_location(location_id)
