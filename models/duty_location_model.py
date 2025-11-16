"""
Duty Location Model
Handles saved duty location data access
"""

import json
from .db import get_connection


class DutyLocationModel:
    """Model for duty location operations"""
    
    @staticmethod
    def get_all_duty_locations():
        """Get all saved duty locations"""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT * FROM duty_locations
                    ORDER BY created_at DESC
                """
                cursor.execute(query)
                locations = cursor.fetchall()
                
                # Parse JSON polygon field and format for frontend
                for loc in locations:
                    if loc.get('polygon'):
                        loc['polygon'] = json.loads(loc['polygon'])
                    
                    # Convert center_lat/center_lng to center array
                    loc['center'] = [float(loc['center_lat']), float(loc['center_lng'])]
                    
                    # Convert snake_case to camelCase for frontend compatibility
                    if 'created_at' in loc:
                        loc['createdAt'] = loc['created_at'].isoformat() if hasattr(loc['created_at'], 'isoformat') else str(loc['created_at'])
                    if 'updated_at' in loc:
                        loc['updatedAt'] = loc['updated_at'].isoformat() if hasattr(loc['updated_at'], 'isoformat') else str(loc['updated_at'])
                
                return locations
    
    @staticmethod
    def get_duty_location_by_id(location_id):
        """Get duty location by ID"""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT * FROM duty_locations WHERE id = %s"
                cursor.execute(query, (location_id,))
                location = cursor.fetchone()
                
                if location:
                    if location.get('polygon'):
                        location['polygon'] = json.loads(location['polygon'])
                    
                    # Convert center_lat/center_lng to center array
                    location['center'] = [float(location['center_lat']), float(location['center_lng'])]
                    
                    # Convert snake_case to camelCase for frontend compatibility
                    if 'created_at' in location:
                        location['createdAt'] = location['created_at'].isoformat() if hasattr(location['created_at'], 'isoformat') else str(location['created_at'])
                    if 'updated_at' in location:
                        location['updatedAt'] = location['updated_at'].isoformat() if hasattr(location['updated_at'], 'isoformat') else str(location['updated_at'])
                
                return location
    
    @staticmethod
    def get_duty_location_by_name(name):
        """Get duty location by name"""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT * FROM duty_locations WHERE name = %s"
                cursor.execute(query, (name,))
                location = cursor.fetchone()
                
                if location:
                    if location.get('polygon'):
                        location['polygon'] = json.loads(location['polygon'])
                    location['center'] = [location['center_lat'], location['center_lng']]
                
                return location
    
    @staticmethod
    def create_duty_location(location_data):
        """Create new duty location"""
        import uuid
        from datetime import datetime
        
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO duty_locations 
                    (id, name, center_lat, center_lng, radius, polygon, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                # Generate ID if not provided
                location_id = location_data.get('id') or str(uuid.uuid4())
                center = location_data.get('center', [0, 0])
                polygon = json.dumps(location_data.get('polygon', []))
                now = datetime.now().isoformat()
                
                cursor.execute(query, (
                    location_id,
                    location_data['name'],
                    center[0],
                    center[1],
                    location_data.get('radius', 100),
                    polygon,
                    location_data.get('createdAt') or now,
                    location_data.get('updatedAt') or now
                ))
                conn.commit()
                return location_id
    
    @staticmethod
    def update_duty_location(location_id, updates):
        """Update duty location"""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                fields = []
                values = []
                
                if 'name' in updates:
                    fields.append("name = %s")
                    values.append(updates['name'])
                
                if 'radius' in updates:
                    fields.append("radius = %s")
                    values.append(updates['radius'])
                
                fields.append("updated_at = NOW()")
                values.append(location_id)
                
                query = f"UPDATE duty_locations SET {', '.join(fields)} WHERE id = %s"
                cursor.execute(query, values)
                conn.commit()
                return cursor.rowcount > 0
    
    @staticmethod
    def delete_duty_location(location_id):
        """Delete duty location"""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM duty_locations WHERE id = %s", (location_id,))
                conn.commit()
                return cursor.rowcount > 0
