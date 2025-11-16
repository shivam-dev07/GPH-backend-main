"""
Duty Location Controller
Handles saved duty location business logic
"""

from models.duty_location_model import DutyLocationModel
from utils.logger import log_info, log_error
from utils.responses import success_response, error_response


class DutyLocationController:
    """Controller for duty location operations"""
    
    @staticmethod
    def get_all_duty_locations():
        """Get all saved duty locations"""
        try:
            log_info("Fetching all duty locations")
            locations = DutyLocationModel.get_all_duty_locations()
            return success_response(locations)
        except Exception as e:
            log_error(f"Error fetching duty locations: {str(e)}")
            return error_response("Failed to fetch duty locations", 500)
    
    @staticmethod
    def get_duty_location(location_id):
        """Get duty location by ID"""
        try:
            log_info(f"Fetching duty location: {location_id}")
            location = DutyLocationModel.get_duty_location_by_id(location_id)
            
            if not location:
                return error_response("Duty location not found", 404)
            
            return success_response(location)
        except Exception as e:
            log_error(f"Error fetching duty location {location_id}: {str(e)}")
            return error_response("Failed to fetch duty location", 500)
    
    @staticmethod
    def create_duty_location(location_data):
        """Create new duty location"""
        try:
            log_info(f"Creating duty location with data: {location_data}")
            
            # Validate required fields
            if not location_data.get('name'):
                return error_response("Location name is required", 400)
            
            location_id = DutyLocationModel.create_duty_location(location_data)
            return success_response({'id': location_id}, 201)
        except Exception as e:
            import traceback
            log_error(f"Error creating duty location: {str(e)}\nTraceback: {traceback.format_exc()}")
            return error_response(f"Failed to create duty location: {str(e)}", 500)
    
    @staticmethod
    def update_duty_location(location_id, updates):
        """Update duty location"""
        try:
            log_info(f"Updating duty location: {location_id}")
            success = DutyLocationModel.update_duty_location(location_id, updates)
            
            if not success:
                return error_response("Duty location not found", 404)
            
            return success_response({"message": "Success"})
        except Exception as e:
            log_error(f"Error updating duty location {location_id}: {str(e)}")
            return error_response("Failed to update duty location", 500)
    
    @staticmethod
    def delete_duty_location(location_id):
        """Delete duty location"""
        try:
            log_info(f"Deleting duty location: {location_id}")
            success = DutyLocationModel.delete_duty_location(location_id)
            
            if not success:
                return error_response("Duty location not found", 404)
            
            return success_response({"message": "Success"})
        except Exception as e:
            log_error(f"Error deleting duty location {location_id}: {str(e)}")
            return error_response("Failed to delete duty location", 500)
