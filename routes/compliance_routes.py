"""
Compliance Routes
API endpoints for compliance log operations
"""

from flask import Blueprint, request
from controllers.compliance_controller import ComplianceController

compliance_bp = Blueprint('compliance', __name__, url_prefix='/api/compliance')


@compliance_bp.route('', methods=['GET'])
def get_all_compliance_logs():
    """GET /api/compliance?limit=100 - Get all compliance logs"""
    limit = request.args.get('limit', 100, type=int)
    return ComplianceController.get_all_compliance_logs(limit)


@compliance_bp.route('/duty/<duty_id>', methods=['GET'])
def get_compliance_by_duty(duty_id):
    """GET /api/compliance/duty/:dutyId - Get compliance logs by duty"""
    return ComplianceController.get_compliance_by_duty(duty_id)


@compliance_bp.route('', methods=['POST'])
def create_compliance_log():
    """POST /api/compliance - Create new compliance log"""
    log_data = request.get_json()
    return ComplianceController.create_compliance_log(log_data)
