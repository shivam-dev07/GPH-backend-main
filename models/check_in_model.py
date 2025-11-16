"""
Check-in Model
Handles duty check-in/check-out data access
"""

import json
from .db import get_connection


class CheckInModel:
    """Model for check-in operations"""
    
    @staticmethod
    def get_all_check_ins(limit=100):
        """Get all check-ins"""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        ci.*,
                        o.staff_name as officer_name
                    FROM check_ins ci
                    LEFT JOIN officers o ON ci.officer_id = o.id
                    ORDER BY ci.timestamp DESC
                    LIMIT %s
                """
                cursor.execute(query, (limit,))
                check_ins = cursor.fetchall()
                
                # Parse JSON fields
                for ci in check_ins:
                    if ci.get('location'):
                        ci['location'] = json.loads(ci['location'])
                    if ci.get('device_info'):
                        ci['device_info'] = json.loads(ci['device_info'])
                
                return check_ins
    
    @staticmethod
    def get_check_ins_by_duty(duty_id):
        """Get check-ins for specific duty"""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        ci.*,
                        o.staff_name as officer_name
                    FROM check_ins ci
                    LEFT JOIN officers o ON ci.officer_id = o.id
                    WHERE ci.duty_id = %s
                    ORDER BY ci.timestamp ASC
                """
                cursor.execute(query, (duty_id,))
                check_ins = cursor.fetchall()
                
                for ci in check_ins:
                    if ci.get('location'):
                        ci['location'] = json.loads(ci['location'])
                    if ci.get('device_info'):
                        ci['device_info'] = json.loads(ci['device_info'])
                
                return check_ins
    
    @staticmethod
    def create_check_in(check_in_data):
        """Create new check-in"""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO check_ins 
                    (id, officer_id, officer_uid, duty_id, check_in_type, location, 
                     selfie_image_url, device_info, verified, verification_method, 
                     compliance_score, timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                location = json.dumps(check_in_data.get('location', {}))
                device_info = json.dumps(check_in_data.get('deviceInfo', {}))
                
                cursor.execute(query, (
                    check_in_data['id'],
                    check_in_data.get('officerId') or check_in_data.get('officerUid'),
                    check_in_data.get('officerUid'),
                    check_in_data['dutyId'],
                    check_in_data['checkInType'],
                    location,
                    check_in_data.get('selfieImageUrl'),
                    device_info,
                    check_in_data.get('verified', False),
                    check_in_data.get('verificationMethod', 'geolocation'),
                    check_in_data.get('complianceScore', 0),
                    check_in_data['timestamp']
                ))
                conn.commit()
                return check_in_data['id']
