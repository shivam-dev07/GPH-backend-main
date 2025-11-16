"""
Compliance Controller
Handles compliance log business logic
"""

from models.compliance_model import ComplianceModel
from utils.logger import log_info, log_error
from utils.responses import success_response, error_response


class ComplianceController:
    """Controller for compliance operations"""
    
    @staticmethod
    def get_all_compliance_logs(limit=100):
        """Get all compliance logs"""
        try:
            log_info(f"Fetching compliance logs (limit: {limit})")
            logs = ComplianceModel.get_all_compliance_logs(limit)
            return success_response(logs)
        except Exception as e:
            log_error(f"Error fetching compliance logs: {str(e)}")
            return error_response("Failed to fetch compliance logs", 500)
    
    @staticmethod
    def get_compliance_by_duty(duty_id):
        """Get compliance logs for specific duty"""
        try:
            log_info(f"Fetching compliance logs for duty: {duty_id}")
            logs = ComplianceModel.get_compliance_by_duty(duty_id)
            return success_response(logs)
        except Exception as e:
            log_error(f"Error fetching compliance logs for duty {duty_id}: {str(e)}")
            return error_response("Failed to fetch compliance logs", 500)
    
    @staticmethod
    def create_compliance_log(log_data):
        """Create new compliance log"""
        try:
            log_info(f"Creating compliance log: {log_data.get('id')}")
            log_id = ComplianceModel.create_compliance_log(log_data)
            return success_response({'id': log_id})
        except Exception as e:
            log_error(f"Error creating compliance log: {str(e)}")
            return error_response("Failed to create compliance log", 500)
