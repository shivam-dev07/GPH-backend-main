"""
Live Location Controller
Handles real-time location tracking business logic
"""

from models.live_location_model import LiveLocationModel
from utils.logger import log_info, log_error
from utils.responses import success_response, error_response


class LiveLocationController:
    """Controller for live location operations"""
    
    @staticmethod
    def get_all_live_locations():
        """Get all live officer locations"""
        try:
            log_info("Fetching all live locations")
            locations = LiveLocationModel.get_all_live_locations()
            return success_response(locations)
        except Exception as e:
            log_error(f"Error fetching live locations: {str(e)}")
            return error_response("Failed to fetch live locations", 500)
    
    @staticmethod
    def get_location_by_officer(officer_id):
        """Get live location for specific officer"""
        try:
            log_info(f"Fetching live location for officer: {officer_id}")
            location = LiveLocationModel.get_location_by_officer(officer_id)
            
            if not location:
                return error_response("Location not found", 404)
            
            return success_response(location)
        except Exception as e:
            log_error(f"Error fetching location for officer {officer_id}: {str(e)}")
            return error_response("Failed to fetch location", 500)
    
    @staticmethod
    def update_location(officer_id, location_data):
        """Update officer's live location"""
        try:
            log_info(f"Updating location for officer: {officer_id}")
            success = LiveLocationModel.update_location(officer_id, location_data)
            return success_response({"message": "Success"})
        except Exception as e:
            log_error(f"Error updating location for officer {officer_id}: {str(e)}")
            return error_response("Failed to update location", 500)
