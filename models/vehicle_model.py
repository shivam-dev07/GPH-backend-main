"""
Vehicle Model
Handles vehicle data access
"""

from .db import get_connection


class VehicleModel:
    """Model for vehicle operations"""
    
    @staticmethod
    def get_all_vehicles():
        """Get all vehicles"""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT * FROM vehicles 
                    ORDER BY vehicle_name ASC
                """
                cursor.execute(query)
                return cursor.fetchall()
    
    @staticmethod
    def get_vehicle_by_id(vehicle_id):
        """Get vehicle by ID"""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT * FROM vehicles WHERE id = %s"
                cursor.execute(query, (vehicle_id,))
                return cursor.fetchone()
    
    @staticmethod
    def create_vehicle(vehicle_data):
        """Create new vehicle"""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO vehicles (id, vehicle_name, vehicle_number, status)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (
                    vehicle_data['id'],
                    vehicle_data['vehicle_name'],
                    vehicle_data['vehicle_number'],
                    vehicle_data.get('status', 'available')
                ))
                conn.commit()
                return vehicle_data['id']
    
    @staticmethod
    def update_vehicle(vehicle_id, updates):
        """Update vehicle"""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                fields = []
                values = []
                
                if 'vehicle_name' in updates:
                    fields.append("vehicle_name = %s")
                    values.append(updates['vehicle_name'])
                
                if 'vehicle_number' in updates:
                    fields.append("vehicle_number = %s")
                    values.append(updates['vehicle_number'])
                
                if 'status' in updates:
                    fields.append("status = %s")
                    values.append(updates['status'])
                
                values.append(vehicle_id)
                query = f"UPDATE vehicles SET {', '.join(fields)} WHERE id = %s"
                cursor.execute(query, values)
                conn.commit()
                return cursor.rowcount > 0
    
    @staticmethod
    def delete_vehicle(vehicle_id):
        """Delete vehicle"""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM vehicles WHERE id = %s", (vehicle_id,))
                conn.commit()
                return cursor.rowcount > 0
