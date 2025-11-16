"""
Notification Routes
API endpoints for notification operations
"""

from flask import Blueprint, request
from controllers.notification_controller import NotificationController

notification_bp = Blueprint('notification', __name__, url_prefix='/api/notifications')


@notification_bp.route('/officer/<officer_id>', methods=['GET'])
def get_notifications_by_officer(officer_id):
    """GET /api/notifications/officer/:officerId - Get notifications for officer"""
    include_deleted = request.args.get('includeDeleted', 'false').lower() == 'true'
    return NotificationController.get_notifications_by_officer(officer_id, include_deleted)


@notification_bp.route('', methods=['POST'])
def create_notification():
    """POST /api/notifications - Create new notification"""
    notif_data = request.get_json()
    return NotificationController.create_notification(notif_data)


@notification_bp.route('/<notification_id>/read', methods=['PUT', 'PATCH'])
def mark_as_read(notification_id):
    """PUT/PATCH /api/notifications/:id/read - Mark notification as read"""
    return NotificationController.mark_as_read(notification_id)


@notification_bp.route('/<notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    """DELETE /api/notifications/:id - Delete notification"""
    return NotificationController.delete_notification(notification_id)
