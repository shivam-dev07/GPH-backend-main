"""
Vehicle Controller
Handles vehicle business logic
"""

from models.vehicle_model import VehicleModel
from utils.logger import log_info, log_error
from utils.responses import success_response, error_response


class VehicleController:
    """Controller for vehicle operations"""
    
    @staticmethod
    def get_all_vehicles():
        """Get all vehicles"""
        try:
            log_info("Fetching all vehicles")
            vehicles = VehicleModel.get_all_vehicles()
            return success_response(vehicles)
        except Exception as e:
            log_error(f"Error fetching vehicles: {str(e)}")
            return error_response("Failed to fetch vehicles", 500)
    
    @staticmethod
    def get_vehicle(vehicle_id):
        """Get vehicle by ID"""
        try:
            log_info(f"Fetching vehicle: {vehicle_id}")
            vehicle = VehicleModel.get_vehicle_by_id(vehicle_id)
            
            if not vehicle:
                return error_response("Vehicle not found", 404)
            
            return success_response(vehicle)
        except Exception as e:
            log_error(f"Error fetching vehicle {vehicle_id}: {str(e)}")
            return error_response("Failed to fetch vehicle", 500)
    
    @staticmethod
    def create_vehicle(vehicle_data):
        """Create new vehicle"""
        try:
            log_info(f"Creating vehicle: {vehicle_data.get('id')}")
            vehicle_id = VehicleModel.create_vehicle(vehicle_data)
            return success_response({'id': vehicle_id}, 201)
        except Exception as e:
            log_error(f"Error creating vehicle: {str(e)}")
            return error_response("Failed to create vehicle", 500)
    
    @staticmethod
    def update_vehicle(vehicle_id, updates):
        """Update vehicle"""
        try:
            log_info(f"Updating vehicle: {vehicle_id}")
            success = VehicleModel.update_vehicle(vehicle_id, updates)
            
            if not success:
                return error_response("Vehicle not found", 404)
            
            return success_response({"message": "Vehicle updated"})
        except Exception as e:
            log_error(f"Error updating vehicle {vehicle_id}: {str(e)}")
            return error_response("Failed to update vehicle", 500)
    
    @staticmethod
    def delete_vehicle(vehicle_id):
        """Delete vehicle"""
        try:
            log_info(f"Deleting vehicle: {vehicle_id}")
            success = VehicleModel.delete_vehicle(vehicle_id)
            
            if not success:
                return error_response("Vehicle not found", 404)
            
            return success_response({"message": "Vehicle deleted"})
        except Exception as e:
            log_error(f"Error deleting vehicle {vehicle_id}: {str(e)}")
            return error_response("Failed to delete vehicle", 500)
