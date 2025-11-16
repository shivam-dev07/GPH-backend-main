"""
Check-in Controller
Handles check-in business logic
"""

from models.check_in_model import CheckInModel
from utils.logger import log_info, log_error
from utils.responses import success_response, error_response


class CheckInController:
    """Controller for check-in operations"""
    
    @staticmethod
    def get_all_check_ins(limit=100):
        """Get all check-ins"""
        try:
            log_info(f"Fetching check-ins (limit: {limit})")
            check_ins = CheckInModel.get_all_check_ins(limit)
            return success_response(check_ins)
        except Exception as e:
            log_error(f"Error fetching check-ins: {str(e)}")
            return error_response("Failed to fetch check-ins", 500)
    
    @staticmethod
    def get_check_ins_by_duty(duty_id):
        """Get check-ins for specific duty"""
        try:
            log_info(f"Fetching check-ins for duty: {duty_id}")
            check_ins = CheckInModel.get_check_ins_by_duty(duty_id)
            return success_response(check_ins)
        except Exception as e:
            log_error(f"Error fetching check-ins for duty {duty_id}: {str(e)}")
            return error_response("Failed to fetch check-ins", 500)
    
    @staticmethod
    def create_check_in(check_in_data):
        """Create new check-in"""
        try:
            log_info(f"Creating check-in: {check_in_data.get('id')}")
            check_in_id = CheckInModel.create_check_in(check_in_data)
            return success_response({'id': check_in_id})
        except Exception as e:
            log_error(f"Error creating check-in: {str(e)}")
            return error_response("Failed to create check-in", 500)
