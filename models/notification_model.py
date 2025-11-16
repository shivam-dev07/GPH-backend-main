"""
Notification Model
Handles notification data access
"""

import json
from .db import get_connection


class NotificationModel:
    """Model for notification operations"""
    
    @staticmethod
    def get_notifications_by_officer(officer_id, include_deleted=False):
        """Get notifications for specific officer"""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT * FROM notifications
                    WHERE officer_id = %s
                """
                
                if not include_deleted:
                    query += " AND deleted = FALSE"
                
                query += " ORDER BY sent_at DESC LIMIT 100"
                
                cursor.execute(query, (officer_id,))
                notifications = cursor.fetchall()
                
                # Parse JSON fields
                for notif in notifications:
                    if notif.get('data'):
                        notif['data'] = json.loads(notif['data'])
                    if notif.get('location_polygon'):
                        notif['location_polygon'] = json.loads(notif['location_polygon'])
                    if notif.get('vehicle_ids'):
                        notif['vehicle_ids'] = json.loads(notif['vehicle_ids'])
                
                return notifications
    
    @staticmethod
    def create_notification(notif_data):
        """Create new notification"""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO notifications 
                    (id, officer_id, type, title, body, message, data, duty_type, duty_id,
                     location_polygon, vehicle_ids, start_time, end_time, status, comments,
                     `read`, sent_at, timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                data = json.dumps(notif_data.get('data', {}))
                location_polygon = json.dumps(notif_data.get('location_polygon', []))
                vehicle_ids = json.dumps(notif_data.get('vehicle_ids', []))
                
                cursor.execute(query, (
                    notif_data['id'],
                    notif_data.get('officerId') or notif_data.get('officerUid'),
                    notif_data.get('type', 'duty'),
                    notif_data['title'],
                    notif_data.get('body'),
                    notif_data.get('message'),
                    data,
                    notif_data.get('duty_type'),
                    notif_data.get('data', {}).get('dutyId'),
                    location_polygon,
                    vehicle_ids,
                    notif_data.get('start_time'),
                    notif_data.get('end_time'),
                    notif_data.get('status'),
                    notif_data.get('comments'),
                    notif_data.get('read', False),
                    notif_data.get('sentAt'),
                    notif_data.get('timestamp')
                ))
                conn.commit()
                return notif_data['id']
    
    @staticmethod
    def mark_as_read(notification_id):
        """Mark notification as read"""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    UPDATE notifications 
                    SET `read` = TRUE, read_at = NOW()
                    WHERE id = %s
                """
                cursor.execute(query, (notification_id,))
                conn.commit()
                return cursor.rowcount > 0
    
    @staticmethod
    def delete_notification(notification_id):
        """Soft delete notification"""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    UPDATE notifications 
                    SET deleted = TRUE, deleted_at = NOW()
                    WHERE id = %s
                """
                cursor.execute(query, (notification_id,))
                conn.commit()
                return cursor.rowcount > 0
