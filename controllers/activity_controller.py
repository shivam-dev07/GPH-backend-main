"""
Activity Controller
Handles activity business logic
"""

from models.activity_model import ActivityModel
from utils.logger import log_info, log_error
from utils.responses import success_response, error_response


class ActivityController:
    """Controller for activity operations"""
    
    @staticmethod
    def get_all_activities(limit=100):
        """Get all activities with limit"""
        try:
            log_info(f"Fetching activities (limit: {limit})")
            activities = ActivityModel.get_all_activities(limit)
            return success_response(activities)
        except Exception as e:
            log_error(f"Error fetching activities: {str(e)}")
            return error_response("Failed to fetch activities", 500)
    
    @staticmethod
    def get_recent_activities(limit=50):
        """Get recent activities"""
        try:
            log_info(f"Fetching recent activities (limit: {limit})")
            activities = ActivityModel.get_recent_activities(limit)
            return success_response(activities)
        except Exception as e:
            log_error(f"Error fetching recent activities: {str(e)}")
            return error_response("Failed to fetch recent activities", 500)
    
    @staticmethod
    def get_activities_by_duty(duty_id):
        """Get activities for specific duty"""
        try:
            log_info(f"Fetching activities for duty: {duty_id}")
            activities = ActivityModel.get_activities_by_duty(duty_id)
            return success_response(activities)
        except Exception as e:
            log_error(f"Error fetching activities for duty {duty_id}: {str(e)}")
            return error_response("Failed to fetch activities", 500)
    
    @staticmethod
    def get_activities_by_officer(officer_id):
        """Get activities for specific officer"""
        try:
            log_info(f"Fetching activities for officer: {officer_id}")
            activities = ActivityModel.get_activities_by_officer(officer_id)
            return success_response(activities)
        except Exception as e:
            log_error(f"Error fetching activities for officer {officer_id}: {str(e)}")
            return error_response("Failed to fetch activities", 500)
    
    @staticmethod
    def create_activity(activity_data):
        """Create new activity"""
        try:
            log_info(f"Creating activity: {activity_data.get('id')}")
            activity_id = ActivityModel.create_activity(activity_data)
            return success_response({'id': activity_id})
        except Exception as e:
            log_error(f"Error creating activity: {str(e)}")
            return error_response("Failed to create activity", 500)
