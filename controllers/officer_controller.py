"""
Officer Controller
Handles officer business logic
"""

from models.officer_model import OfficerModel
from utils.logger import log_info, log_error
from utils.responses import success_response, error_response


class OfficerController:
    """Controller for officer operations"""
    
    @staticmethod
    def get_all_officers():
        """Get all officers"""
        try:
            log_info("Fetching all officers")
            officers = OfficerModel.get_all_officers()
            return success_response(officers)
        except Exception as e:
            log_error(f"Error fetching officers: {str(e)}")
            return error_response("Failed to fetch officers", 500)
    
    @staticmethod
    def get_officer(officer_id):
        """Get single officer by ID"""
        try:
            log_info(f"Fetching officer: {officer_id}")
            officer = OfficerModel.get_officer_by_id(officer_id)
            
            if not officer:
                return error_response("Officer not found", 404)
            
            return success_response(officer)
        except Exception as e:
            log_error(f"Error fetching officer {officer_id}: {str(e)}")
            return error_response("Failed to fetch officer", 500)
    
    @staticmethod
    def create_officer(data):
        """Create a new officer"""
        try:
            # Validate required fields
            if not data.get('staff_id') or not data.get('staff_name') or not data.get('staff_designation'):
                return error_response("Missing required fields: staff_id, staff_name, staff_designation", 400)
            
            log_info(f"Creating officer: {data.get('staff_name')}")
            officer_id = OfficerModel.create_officer(data)
            
            # Fetch the created officer to return complete data
            officer = OfficerModel.get_officer_by_id(officer_id)
            return success_response(officer, 201)
        except Exception as e:
            log_error(f"Error creating officer: {str(e)}")
            return error_response("Failed to create officer", 500)
    
    @staticmethod
    def update_officer(officer_id, data):
        """Update an existing officer"""
        try:
            log_info(f"Updating officer: {officer_id}")
            success = OfficerModel.update_officer(officer_id, data)
            
            if not success:
                return error_response("Officer not found", 404)
            
            # Fetch updated officer
            officer = OfficerModel.get_officer_by_id(officer_id)
            return success_response(officer)
        except Exception as e:
            log_error(f"Error updating officer {officer_id}: {str(e)}")
            return error_response("Failed to update officer", 500)
    
    @staticmethod
    def delete_officer(officer_id):
        """Delete an officer"""
        try:
            log_info(f"Deleting officer: {officer_id}")
            success = OfficerModel.delete_officer(officer_id)
            
            if not success:
                return error_response("Officer not found", 404)
            
            return success_response({"message": "Officer deleted successfully"})
        except Exception as e:
            log_error(f"Error deleting officer {officer_id}: {str(e)}")
            return error_response("Failed to delete officer", 500)