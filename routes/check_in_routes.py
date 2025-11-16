"""
Check-in Routes
API endpoints for check-in operations
"""

from flask import Blueprint, request
from controllers.check_in_controller import CheckInController

check_in_bp = Blueprint('check_in', __name__, url_prefix='/api/check-ins')


@check_in_bp.route('', methods=['GET'])
def get_all_check_ins():
    """GET /api/check-ins?limit=100 - Get all check-ins"""
    limit = request.args.get('limit', 100, type=int)
    return CheckInController.get_all_check_ins(limit)


@check_in_bp.route('/duty/<duty_id>', methods=['GET'])
def get_check_ins_by_duty(duty_id):
    """GET /api/check-ins/duty/:dutyId - Get check-ins by duty"""
    return CheckInController.get_check_ins_by_duty(duty_id)


@check_in_bp.route('', methods=['POST'])
def create_check_in():
    """POST /api/check-ins - Create new check-in"""
    check_in_data = request.get_json()
    return CheckInController.create_check_in(check_in_data)
