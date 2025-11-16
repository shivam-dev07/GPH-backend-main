"""
Duty Controller
Handles duty business logic
"""

from models.duty_model import DutyModel
from utils.logger import log_info, log_error
from utils.responses import success_response, error_response


class DutyController:
    """Controller for duty operations"""
    
    @staticmethod
    def get_all_duties():
        """Get all duties"""
        try:
            log_info("Fetching all duties")
            duties = DutyModel.get_all_duties()
            return success_response(duties)
        except Exception as e:
            log_error(f"Error fetching duties: {str(e)}")
            return error_response("Failed to fetch duties", 500)
    
    @staticmethod
    def get_duty(duty_id):
        """Get single duty by ID"""
        try:
            log_info(f"Fetching duty: {duty_id}")
            duty = DutyModel.get_duty_by_id(duty_id)
            
            if not duty:
                return error_response("Duty not found", 404)
            
            return success_response(duty)
        except Exception as e:
            log_error(f"Error fetching duty {duty_id}: {str(e)}")
            return error_response("Failed to fetch duty", 500)
    
    @staticmethod
    def get_active_duties():
        """Get all active duties"""
        try:
            log_info("Fetching active duties")
            duties = DutyModel.get_active_duties()
            return success_response(duties)
        except Exception as e:
            log_error(f"Error fetching active duties: {str(e)}")
            return error_response("Failed to fetch active duties", 500)
    
    @staticmethod
    def get_duties_by_officer(officer_id):
        """Get all duties for a specific officer"""
        try:
            log_info(f"Fetching duties for officer: {officer_id}")
            duties = DutyModel.get_duties_by_officer(officer_id)
            return success_response(duties)
        except Exception as e:
            log_error(f"Error fetching duties for officer {officer_id}: {str(e)}")
            return error_response("Failed to fetch officer duties", 500)
    
    @staticmethod
    def create_duty(duty_data):
        """Create new duty"""
        try:
            log_info(f"Creating duty with data: {duty_data}")
            duty_id = DutyModel.create_duty(duty_data)
            return success_response({'id': duty_id}, 201)
        except Exception as e:
            import traceback
            log_error(f"Error creating duty: {str(e)}\nTraceback: {traceback.format_exc()}")
            return error_response(f"Failed to create duty: {str(e)}", 500)
    
    @staticmethod
    def update_duty(duty_id, updates):
        """Update duty"""
        try:
            log_info(f"Updating duty: {duty_id}")
            success = DutyModel.update_duty(duty_id, updates)
            
            if not success:
                return error_response("Duty not found", 404)
            
            return success_response({"message": "Success"})
        except Exception as e:
            log_error(f"Error updating duty {duty_id}: {str(e)}")
            return error_response("Failed to update duty", 500)
    
    @staticmethod
    def delete_duty(duty_id):
        """Delete duty"""
        try:
            log_info(f"Deleting duty: {duty_id}")
            success = DutyModel.delete_duty(duty_id)
            
            if not success:
                return error_response("Duty not found", 404)
            
            return success_response({"message": "Duty deleted"})
        except Exception as e:
            log_error(f"Error deleting duty {duty_id}: {str(e)}")
            return error_response("Failed to delete duty", 500)
