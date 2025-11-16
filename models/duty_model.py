"""
Duty Model
Handles duty data access with parameterized queries
"""

import json
from .db import get_connection


class DutyModel:
    """Model for duty operations"""
    
    @staticmethod
    def get_all_duties():
        """
        Get all duties with officer and vehicle information.
        
        Returns:
            list: List of duty dictionaries with all fields
        """
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        d.*,
                        GROUP_CONCAT(DISTINCT do.officer_id ORDER BY do.officer_id SEPARATOR ',') as officer_uids,
                        GROUP_CONCAT(DISTINCT o.staff_name ORDER BY do.officer_id SEPARATOR ', ') as officer_names,
                        GROUP_CONCAT(DISTINCT dv.vehicle_id ORDER BY dv.vehicle_id SEPARATOR ',') as vehicle_ids
                    FROM duties d
                    LEFT JOIN duty_officers do ON d.id = do.duty_id
                    LEFT JOIN officers o ON do.officer_id = o.id
                    LEFT JOIN duty_vehicles dv ON d.id = dv.duty_id
                    GROUP BY d.id
                    ORDER BY d.created_at DESC
                """
                cursor.execute(query)
                duties = cursor.fetchall()
                
                # Parse JSON fields and split arrays
                for duty in duties:
                    # Always create location object
                    if duty['location_polygon']:
                        try:
                            polygon_data = json.loads(duty['location_polygon'])
                        except:
                            polygon_data = []
                    else:
                        polygon_data = []
                    
                    duty['location'] = {
                        'polygon': polygon_data,
                        'radius': duty['location_radius'] or 500
                    }
                    
                    duty['officerUids'] = duty['officer_uids'].split(',') if duty['officer_uids'] else []
                    duty['officerNames'] = duty['officer_names'] if duty['officer_names'] else ''
                    duty['vehicleIds'] = duty['vehicle_ids'].split(',') if duty['vehicle_ids'] else []
                    
                return duties
    
    @staticmethod
    def get_duty_by_id(duty_id):
        """
        Get duty by ID with officer and vehicle information.
        
        Args:
            duty_id (str): Duty ID to fetch
            
        Returns:
            dict: Duty dictionary or None if not found
        """
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        d.*,
                        GROUP_CONCAT(DISTINCT do.officer_id ORDER BY do.officer_id SEPARATOR ',') as officer_uids,
                        GROUP_CONCAT(DISTINCT o.staff_name ORDER BY do.officer_id SEPARATOR ', ') as officer_names,
                        GROUP_CONCAT(DISTINCT dv.vehicle_id ORDER BY dv.vehicle_id SEPARATOR ',') as vehicle_ids
                    FROM duties d
                    LEFT JOIN duty_officers do ON d.id = do.duty_id
                    LEFT JOIN officers o ON do.officer_id = o.id
                    LEFT JOIN duty_vehicles dv ON d.id = dv.duty_id
                    WHERE d.id = %s
                    GROUP BY d.id
                """
                cursor.execute(query, (duty_id,))
                duty = cursor.fetchone()
                
                if duty:
                    # Always create location object
                    if duty['location_polygon']:
                        try:
                            polygon_data = json.loads(duty['location_polygon'])
                        except:
                            polygon_data = []
                    else:
                        polygon_data = []
                    
                    duty['location'] = {
                        'polygon': polygon_data,
                        'radius': duty['location_radius'] or 500
                    }
                    
                    duty['officerUids'] = duty['officer_uids'].split(',') if duty['officer_uids'] else []
                    duty['officerNames'] = duty['officer_names'] if duty['officer_names'] else ''
                    duty['vehicleIds'] = duty['vehicle_ids'].split(',') if duty['vehicle_ids'] else []
                
                return duty
    
    @staticmethod
    def get_active_duties():
        """
        Get all active duties.
        
        Returns:
            list: List of active duty dictionaries
        """
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        d.*,
                        GROUP_CONCAT(DISTINCT do.officer_id ORDER BY do.officer_id SEPARATOR ',') as officer_uids,
                        GROUP_CONCAT(DISTINCT o.staff_name ORDER BY do.officer_id SEPARATOR ', ') as officer_names,
                        GROUP_CONCAT(DISTINCT dv.vehicle_id ORDER BY dv.vehicle_id SEPARATOR ',') as vehicle_ids
                    FROM duties d
                    LEFT JOIN duty_officers do ON d.id = do.duty_id
                    LEFT JOIN officers o ON do.officer_id = o.id
                    LEFT JOIN duty_vehicles dv ON d.id = dv.duty_id
                    WHERE d.status IN ('active', 'assigned', 'incomplete')
                    GROUP BY d.id
                    ORDER BY d.start_time DESC
                """
                cursor.execute(query)
                duties = cursor.fetchall()
                
                for duty in duties:
                    # Always create location object
                    if duty['location_polygon']:
                        try:
                            polygon_data = json.loads(duty['location_polygon'])
                        except:
                            polygon_data = []
                    else:
                        polygon_data = []
                    
                    duty['location'] = {
                        'polygon': polygon_data,
                        'radius': duty['location_radius'] or 500
                    }
                    
                    duty['officerUids'] = duty['officer_uids'].split(',') if duty['officer_uids'] else []
                    duty['officerNames'] = duty['officer_names'] if duty['officer_names'] else ''
                    duty['vehicleIds'] = duty['vehicle_ids'].split(',') if duty['vehicle_ids'] else []
                
                return duties
    
    @staticmethod
    def get_duties_by_officer(officer_id):
        """
        Get all duties assigned to a specific officer.
        
        Args:
            officer_id (str): Officer ID to fetch duties for
            
        Returns:
            list: List of duty dictionaries assigned to the officer
        """
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        d.*,
                        GROUP_CONCAT(DISTINCT do.officer_id ORDER BY do.officer_id SEPARATOR ',') as officer_uids,
                        GROUP_CONCAT(DISTINCT o.staff_name ORDER BY do.officer_id SEPARATOR ', ') as officer_names,
                        GROUP_CONCAT(DISTINCT dv.vehicle_id ORDER BY dv.vehicle_id SEPARATOR ',') as vehicle_ids
                    FROM duties d
                    INNER JOIN duty_officers do ON d.id = do.duty_id
                    LEFT JOIN officers o ON do.officer_id = o.id
                    LEFT JOIN duty_vehicles dv ON d.id = dv.duty_id
                    WHERE do.officer_id = %s
                    GROUP BY d.id
                    ORDER BY d.start_time DESC
                """
                cursor.execute(query, (officer_id,))
                duties = cursor.fetchall()
                
                # Parse JSON fields and split arrays
                for duty in duties:
                    # Always create location object
                    if duty['location_polygon']:
                        try:
                            polygon_data = json.loads(duty['location_polygon'])
                        except:
                            polygon_data = []
                    else:
                        polygon_data = []
                    
                    duty['location'] = {
                        'polygon': polygon_data,
                        'radius': duty['location_radius'] or 500
                    }
                    
                    duty['officerUids'] = duty['officer_uids'].split(',') if duty['officer_uids'] else []
                    duty['officerNames'] = duty['officer_names'] if duty['officer_names'] else ''
                    duty['vehicleIds'] = duty['vehicle_ids'].split(',') if duty['vehicle_ids'] else []
                    
                return duties
    
    @staticmethod
    def create_duty(duty_data):
        """
        Create a new duty.
        
        Args:
            duty_data (dict): Duty information
            
        Returns:
            str: Created duty ID
        """
        import uuid
        from datetime import datetime
        
        def convert_iso_to_mysql(iso_string):
            """Convert ISO 8601 datetime string to MySQL datetime format"""
            if not iso_string:
                return None
            try:
                # Parse ISO format (e.g., '2025-11-15T16:00:00.000Z')
                dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
                # Return MySQL format: 'YYYY-MM-DD HH:MM:SS'
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                return iso_string  # Return as-is if parsing fails
        
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Generate ID if not provided
                duty_id = duty_data.get('id') or str(uuid.uuid4())
                
                # Insert duty
                query = """
                    INSERT INTO duties 
                    (id, type, location_polygon, location_radius, start_time, end_time, 
                     status, assigned_at, comments, last_updated)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                # Handle both nested location object and flat location_polygon field
                if 'location_polygon' in duty_data and isinstance(duty_data['location_polygon'], (list, str)):
                    # Direct polygon data provided (from Excel import)
                    if isinstance(duty_data['location_polygon'], str):
                        location_polygon = duty_data['location_polygon']  # Already JSON string
                    else:
                        location_polygon = json.dumps(duty_data['location_polygon'])  # Convert array to JSON
                    location_radius = duty_data.get('location_radius', 500)
                else:
                    # Nested location object (from frontend)
                    location = duty_data.get('location', {})
                    location_polygon = json.dumps(location.get('polygon', []))
                    location_radius = location.get('radius', 500)
                
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Get and convert datetime fields
                start_time = convert_iso_to_mysql(duty_data.get('start_time') or duty_data.get('startTime'))
                end_time = convert_iso_to_mysql(duty_data.get('end_time') or duty_data.get('endTime'))
                assigned_at = convert_iso_to_mysql(duty_data.get('assigned_at') or duty_data.get('assignedAt')) or now
                last_updated = convert_iso_to_mysql(duty_data.get('last_updated') or duty_data.get('lastUpdated')) or now
                
                cursor.execute(query, (
                    duty_id,
                    duty_data.get('type', 'patrol'),
                    location_polygon,
                    location_radius,
                    start_time,
                    end_time,
                    duty_data.get('status', 'assigned'),
                    assigned_at,
                    duty_data.get('comments', ''),
                    last_updated
                ))
                
                # Link officers - support both camelCase and snake_case
                # Handle both UUID ids and staff_ids
                officer_ids = duty_data.get('officerUids') or duty_data.get('officer_uids') or []
                for officer_ref in officer_ids:
                    # Check if this is a staff_id (format like 'GP33239') or UUID
                    if officer_ref and len(str(officer_ref)) < 20:  # Likely a staff_id, not a UUID
                        # Look up the officer's UUID by staff_id
                        cursor.execute(
                            "SELECT id FROM officers WHERE staff_id = %s LIMIT 1",
                            (officer_ref,)
                        )
                        officer_row = cursor.fetchone()
                        if officer_row:
                            officer_id = officer_row['id']
                        else:
                            # Staff ID not found, skip this officer
                            continue
                    else:
                        officer_id = officer_ref
                    
                    cursor.execute(
                        "INSERT INTO duty_officers (duty_id, officer_id) VALUES (%s, %s)",
                        (duty_id, officer_id)
                    )
                
                # Link vehicles - support both camelCase and snake_case
                vehicle_ids = duty_data.get('vehicleIds') or duty_data.get('vehicle_ids') or []
                for vehicle_id in vehicle_ids:
                    cursor.execute(
                        "INSERT INTO duty_vehicles (duty_id, vehicle_id) VALUES (%s, %s)",
                        (duty_id, vehicle_id)
                    )
                
                conn.commit()
                return duty_id
    
    @staticmethod
    def update_duty(duty_id, updates):
        """
        Update duty status or other fields.
        
        Args:
            duty_id (str): Duty ID
            updates (dict): Fields to update
            
        Returns:
            bool: True if successful
        """
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Build dynamic update query
                fields = []
                values = []
                
                if 'status' in updates:
                    fields.append("status = %s")
                    values.append(updates['status'])
                
                if 'checkInTime' in updates:
                    fields.append("check_in_time = %s")
                    values.append(updates['checkInTime'])
                
                if 'checkOutTime' in updates:
                    fields.append("check_out_time = %s")
                    values.append(updates['checkOutTime'])
                
                if 'comments' in updates:
                    fields.append("comments = %s")
                    values.append(updates['comments'])
                
                fields.append("last_updated = NOW()")
                values.append(duty_id)
                
                query = f"UPDATE duties SET {', '.join(fields)} WHERE id = %s"
                cursor.execute(query, values)
                conn.commit()
                
                return cursor.rowcount > 0
    
    @staticmethod
    def delete_duty(duty_id):
        """
        Delete duty (cascade will delete related records).
        
        Args:
            duty_id (str): Duty ID
            
        Returns:
            bool: True if successful
        """
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM duties WHERE id = %s", (duty_id,))
                conn.commit()
                return cursor.rowcount > 0
