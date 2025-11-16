"""
Compliance Model
Handles compliance log data access
"""

import json
from .db import get_connection


class ComplianceModel:
    """Model for compliance operations"""
    
    @staticmethod
    def get_all_compliance_logs(limit=100):
        """Get all compliance logs"""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        c.*,
                        o.staff_name as officer_name
                    FROM compliance c
                    LEFT JOIN officers o ON c.officer_id = o.id
                    ORDER BY c.timestamp DESC
                    LIMIT %s
                """
                cursor.execute(query, (limit,))
                logs = cursor.fetchall()
                
                # Parse JSON location field
                for log in logs:
                    if log.get('location'):
                        log['location'] = json.loads(log['location'])
                
                return logs
    
    @staticmethod
    def get_compliance_by_duty(duty_id):
        """Get compliance logs for a specific duty"""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        c.*,
                        o.staff_name as officer_name
                    FROM compliance c
                    LEFT JOIN officers o ON c.officer_id = o.id
                    WHERE c.duty_id = %s
                    ORDER BY c.timestamp DESC
                """
                cursor.execute(query, (duty_id,))
                logs = cursor.fetchall()
                
                for log in logs:
                    if log.get('location'):
                        log['location'] = json.loads(log['location'])
                
                return logs
    
    @staticmethod
    def create_compliance_log(log_data):
        """Create new compliance log"""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO compliance 
                    (id, duty_id, officer_id, officer_uid, officer_name, action, 
                     location, timestamp, details, photo_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                location = json.dumps(log_data.get('location', {}))
                
                cursor.execute(query, (
                    log_data['id'],
                    log_data.get('dutyId'),
                    log_data.get('officerId') or log_data.get('officerUid'),
                    log_data.get('officerUid'),
                    log_data.get('officerName'),
                    log_data['action'],
                    location,
                    log_data['timestamp'],
                    log_data.get('details'),
                    log_data.get('photoUrl')
                ))
                conn.commit()
                return log_data['id']
