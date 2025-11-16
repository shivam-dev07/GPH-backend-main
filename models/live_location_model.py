"""
Live Location Model
Handles real-time officer location tracking
"""

import json
from .db import get_connection


class LiveLocationModel:
    """Model for live location operations"""
    
    @staticmethod
    def get_all_live_locations():
        """
        Get all live officer locations with latest data.
        
        Returns:
            list: List of live location dictionaries
        """
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        ll.*,
                        o.staff_name as officer_name,
                        o.staff_designation as designation
                    FROM live_locations ll
                    LEFT JOIN officers o ON ll.officer_id = o.id
                    WHERE ll.is_active = TRUE
                    ORDER BY ll.last_updated DESC
                """
                cursor.execute(query)
                locations = cursor.fetchall()
                
                # Parse JSON fields
                for loc in locations:
                    if loc.get('current_location'):
                        loc['currentLocation'] = json.loads(loc['current_location'])
                    if loc.get('location_history'):
                        loc['locationHistory'] = json.loads(loc['location_history'])
                    if loc.get('locations'):
                        loc['locations'] = json.loads(loc['locations'])
                
                return locations
    
    @staticmethod
    def get_location_by_officer(officer_id):
        """Get live location for specific officer"""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        ll.*,
                        o.staff_name as officer_name,
                        o.staff_designation as designation
                    FROM live_locations ll
                    LEFT JOIN officers o ON ll.officer_id = o.id
                    WHERE ll.officer_id = %s
                """
                cursor.execute(query, (officer_id,))
                location = cursor.fetchone()
                
                if location:
                    if location.get('current_location'):
                        location['currentLocation'] = json.loads(location['current_location'])
                    if location.get('location_history'):
                        location['locationHistory'] = json.loads(location['location_history'])
                    if location.get('locations'):
                        location['locations'] = json.loads(location['locations'])
                
                return location
    
    @staticmethod
    def update_location(officer_id, location_data):
        """
        Update officer's live location.
        
        Args:
            officer_id (str): Officer ID
            location_data (dict): Location update data
            
        Returns:
            bool: True if successful
        """
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Check if location exists
                cursor.execute("SELECT id FROM live_locations WHERE officer_id = %s", (officer_id,))
                exists = cursor.fetchone()
                
                current_location = json.dumps(location_data.get('currentLocation', {}))
                locations = json.dumps(location_data.get('locations', []))
                
                if exists:
                    # Update existing
                    query = """
                        UPDATE live_locations 
                        SET latitude = %s, longitude = %s, speed = %s, altitude = %s,
                            heading = %s, accuracy = %s, timestamp = %s, local_time = %s,
                            current_location = %s, locations = %s, total_points = %s,
                            last_updated = NOW(), last_seen = NOW(), status = %s, is_active = %s
                        WHERE officer_id = %s
                    """
                    cursor.execute(query, (
                        location_data.get('latitude'),
                        location_data.get('longitude'),
                        location_data.get('speed', 0),
                        location_data.get('altitude'),
                        location_data.get('heading'),
                        location_data.get('accuracy'),
                        location_data.get('timestamp'),
                        location_data.get('localTime'),
                        current_location,
                        locations,
                        location_data.get('totalPoints', 0),
                        location_data.get('status', 'active'),
                        location_data.get('isActive', True),
                        officer_id
                    ))
                else:
                    # Insert new
                    query = """
                        INSERT INTO live_locations 
                        (id, officer_id, latitude, longitude, speed, altitude, heading, accuracy,
                         timestamp, local_time, current_location, locations, total_points,
                         tracking_started, last_seen, last_updated, status, is_active)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), NOW(), %s, %s)
                    """
                    cursor.execute(query, (
                        officer_id,
                        officer_id,
                        location_data.get('latitude'),
                        location_data.get('longitude'),
                        location_data.get('speed', 0),
                        location_data.get('altitude'),
                        location_data.get('heading'),
                        location_data.get('accuracy'),
                        location_data.get('timestamp'),
                        location_data.get('localTime'),
                        current_location,
                        locations,
                        location_data.get('totalPoints', 0),
                        location_data.get('status', 'active'),
                        location_data.get('isActive', True)
                    ))
                
                conn.commit()
                return True
