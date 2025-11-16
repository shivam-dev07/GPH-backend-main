"""
Activity Routes
API endpoints for activity operations
"""

from flask import Blueprint, request
from controllers.activity_controller import ActivityController

activity_bp = Blueprint('activity', __name__, url_prefix='/api/activities')


@activity_bp.route('', methods=['GET'])
def get_all_activities():
    """GET /api/activities?limit=100 - Get all activities"""
    limit = request.args.get('limit', 100, type=int)
    return ActivityController.get_all_activities(limit)


@activity_bp.route('/recent', methods=['GET'])
def get_recent_activities():
    """GET /api/activities/recent?limit=50 - Get recent activities"""
    limit = request.args.get('limit', 50, type=int)
    return ActivityController.get_recent_activities(limit)


@activity_bp.route('/duty/<duty_id>', methods=['GET'])
def get_activities_by_duty(duty_id):
    """GET /api/activities/duty/:dutyId - Get activities by duty"""
    return ActivityController.get_activities_by_duty(duty_id)


@activity_bp.route('/officer/<officer_id>', methods=['GET'])
def get_activities_by_officer(officer_id):
    """GET /api/activities/officer/:officerId - Get activities by officer"""
    return ActivityController.get_activities_by_officer(officer_id)


@activity_bp.route('', methods=['POST'])
def create_activity():
    """POST /api/activities - Create new activity"""
    activity_data = request.get_json()
    return ActivityController.create_activity(activity_data)
