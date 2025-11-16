"""
Duty Routes
API endpoints for duty operations
"""

from flask import Blueprint, request
from controllers.duty_controller import DutyController

duty_bp = Blueprint('duty', __name__, url_prefix='/api/duties')


@duty_bp.route('', methods=['GET'])
def get_all_duties():
    """GET /api/duties - Get all duties"""
    return DutyController.get_all_duties()


@duty_bp.route('/active', methods=['GET'])
def get_active_duties():
    """GET /api/duties/active - Get active duties"""
    return DutyController.get_active_duties()


@duty_bp.route('/officer/<officer_id>', methods=['GET'])
def get_duties_by_officer(officer_id):
    """GET /api/duties/officer/:officer_id - Get all duties for a specific officer"""
    return DutyController.get_duties_by_officer(officer_id)


@duty_bp.route('/<duty_id>', methods=['GET'])
def get_duty(duty_id):
    """GET /api/duties/:id - Get duty by ID"""
    return DutyController.get_duty(duty_id)


@duty_bp.route('', methods=['POST'])
def create_duty():
    """POST /api/duties - Create new duty"""
    duty_data = request.get_json()
    return DutyController.create_duty(duty_data)


@duty_bp.route('/<duty_id>', methods=['PUT', 'PATCH'])
def update_duty(duty_id):
    """PUT/PATCH /api/duties/:id - Update duty"""
    updates = request.get_json()
    return DutyController.update_duty(duty_id, updates)


@duty_bp.route('/<duty_id>', methods=['DELETE'])
def delete_duty(duty_id):
    """DELETE /api/duties/:id - Delete duty"""
    return DutyController.delete_duty(duty_id)


@duty_bp.route('/check-conflicts', methods=['POST'])
def check_officer_conflicts():
    """POST /api/duties/check-conflicts - Check for officer scheduling conflicts"""
    data = request.get_json()
    return DutyController.check_officer_conflicts(data)
