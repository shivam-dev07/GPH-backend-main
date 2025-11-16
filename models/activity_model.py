"""
Activity Model
Handles activity/log data access
"""

from .db import get_connection


class ActivityModel:
    """Model for activity operations"""
    
    @staticmethod
    def get_all_activities(limit=100):
        """Get all activities with limit"""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        a.*,
                        o.staff_name as officer_name,
                        o.staff_id as officer_staff_id
                    FROM activities a
                    LEFT JOIN officers o ON a.officer_id = o.id
                    ORDER BY a.timestamp DESC
                    LIMIT %s
                """
                cursor.execute(query, (limit,))
                return cursor.fetchall()
    
    @staticmethod
    def get_recent_activities(limit=50):
        """Get recent activities"""
        return ActivityModel.get_all_activities(limit)
    
    @staticmethod
    def get_activities_by_duty(duty_id):
        """Get activities for a specific duty"""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        a.*,
                        o.staff_name as officer_name,
                        o.staff_id as officer_staff_id
                    FROM activities a
                    LEFT JOIN officers o ON a.officer_id = o.id
                    WHERE a.duty_id = %s
                    ORDER BY a.timestamp DESC
                """
                cursor.execute(query, (duty_id,))
                return cursor.fetchall()
    
    @staticmethod
    def get_activities_by_officer(officer_id):
        """Get activities for a specific officer"""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT a.*
                    FROM activities a
                    WHERE a.officer_id = %s
                    ORDER BY a.timestamp DESC
                """
                cursor.execute(query, (officer_id,))
                return cursor.fetchall()
    
    @staticmethod
    def create_activity(activity_data):
        """Create new activity"""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO activities 
                    (id, officer_id, officer_uid, duty_id, type, title, description, location, timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    activity_data['id'],
                    activity_data.get('officerId') or activity_data.get('officerUid'),
                    activity_data.get('officerUid'),
                    activity_data.get('dutyId'),
                    activity_data['type'],
                    activity_data['title'],
                    activity_data.get('description'),
                    activity_data.get('location'),
                    activity_data['timestamp']
                ))
                conn.commit()
                return activity_data['id']
    
    @staticmethod
    def delete_activity(activity_id):
        """Delete activity"""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM activities WHERE id = %s", (activity_id,))
                conn.commit()
                return cursor.rowcount > 0
