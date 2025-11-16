"""
Vehicle Routes
API endpoints for vehicle operations
"""

from flask import Blueprint, request
from controllers.vehicle_controller import VehicleController

vehicle_bp = Blueprint('vehicle', __name__, url_prefix='/api/vehicles')


@vehicle_bp.route('', methods=['GET'])
def get_all_vehicles():
    """GET /api/vehicles - Get all vehicles"""
    return VehicleController.get_all_vehicles()


@vehicle_bp.route('/<vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    """GET /api/vehicles/:id - Get vehicle by ID"""
    return VehicleController.get_vehicle(vehicle_id)


@vehicle_bp.route('', methods=['POST'])
def create_vehicle():
    """POST /api/vehicles - Create new vehicle"""
    vehicle_data = request.get_json()
    return VehicleController.create_vehicle(vehicle_data)


@vehicle_bp.route('/<vehicle_id>', methods=['PUT', 'PATCH'])
def update_vehicle(vehicle_id):
    """PUT/PATCH /api/vehicles/:id - Update vehicle"""
    updates = request.get_json()
    return VehicleController.update_vehicle(vehicle_id, updates)


@vehicle_bp.route('/<vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    """DELETE /api/vehicles/:id - Delete vehicle"""
    return VehicleController.delete_vehicle(vehicle_id)
