"""
Live Location Routes
API endpoints for real-time location tracking
"""

from flask import Blueprint, request
from controllers.live_location_controller import LiveLocationController

live_location_bp = Blueprint('live_location', __name__, url_prefix='/api/live-locations')


@live_location_bp.route('', methods=['GET'])
def get_all_live_locations():
    """GET /api/live-locations - Get all live officer locations"""
    return LiveLocationController.get_all_live_locations()


@live_location_bp.route('/officer/<officer_id>', methods=['GET'])
def get_location_by_officer(officer_id):
    """GET /api/live-locations/officer/:officerId - Get location for officer"""
    return LiveLocationController.get_location_by_officer(officer_id)


@live_location_bp.route('/officer/<officer_id>', methods=['PUT', 'POST'])
def update_location(officer_id):
    """PUT/POST /api/live-locations/officer/:officerId - Update officer location"""
    location_data = request.get_json()
    return LiveLocationController.update_location(officer_id, location_data)
