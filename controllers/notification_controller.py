"""
Notification Controller
Handles notification business logic
"""

from models.notification_model import NotificationModel
from utils.logger import log_info, log_error
from utils.responses import success_response, error_response


class NotificationController:
    """Controller for notification operations"""
    
    @staticmethod
    def get_notifications_by_officer(officer_id, include_deleted=False):
        """Get notifications for specific officer"""
        try:
            log_info(f"Fetching notifications for officer: {officer_id}")
            notifications = NotificationModel.get_notifications_by_officer(officer_id, include_deleted)
            return success_response(notifications)
        except Exception as e:
            log_error(f"Error fetching notifications for officer {officer_id}: {str(e)}")
            return error_response("Failed to fetch notifications", 500)
    
    @staticmethod
    def create_notification(notif_data):
        """Create new notification"""
        try:
            log_info(f"Creating notification: {notif_data.get('id')}")
            notif_id = NotificationModel.create_notification(notif_data)
            return success_response({'id': notif_id})
        except Exception as e:
            log_error(f"Error creating notification: {str(e)}")
            return error_response("Failed to create notification", 500)
    
    @staticmethod
    def mark_as_read(notification_id):
        """Mark notification as read"""
        try:
            log_info(f"Marking notification as read: {notification_id}")
            success = NotificationModel.mark_as_read(notification_id)
            
            if not success:
                return error_response("Notification not found", 404)
            
            return success_response({"message": "Success"})
        except Exception as e:
            log_error(f"Error marking notification as read {notification_id}: {str(e)}")
            return error_response("Failed to mark notification as read", 500)
    
    @staticmethod
    def delete_notification(notification_id):
        """Delete notification"""
        try:
            log_info(f"Deleting notification: {notification_id}")
            success = NotificationModel.delete_notification(notification_id)
            
            if not success:
                return error_response("Notification not found", 404)
            
            return success_response({"message": "Success"})
        except Exception as e:
            log_error(f"Error deleting notification {notification_id}: {str(e)}")
            return error_response("Failed to delete notification", 500)
