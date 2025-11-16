"""
Officer Model
Handles officer data access with parameterized queries
"""

import uuid
from .db import get_connection


class OfficerModel:
    """Model for officer operations"""
    
    @staticmethod
    def get_all_officers():
        """
        Get all officers from database using parameterized query.
        
        Returns:
            list: List of officer dictionaries with all fields
        """
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Using parameterized query for safety
                query = """
                    SELECT 
                        id, 
                        staff_id, 
                        staff_name, 
                        staff_designation, 
                        staff_nature_of_work, 
                        status,
                        created_at,
                        updated_at
                    FROM officers 
                    ORDER BY id ASC
                """
                cursor.execute(query)
                return cursor.fetchall()
    
    @staticmethod
    def get_officer_by_id(officer_id):
        """
        Get officer by ID using parameterized query.
        
        Args:
            officer_id (str): Officer ID to fetch
            
        Returns:
            dict: Officer dictionary or None if not found
        """
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Using parameterized query to prevent SQL injection
                query = """
                    SELECT 
                        id, 
                        staff_id, 
                        staff_name, 
                        staff_designation, 
                        staff_nature_of_work, 
                        status,
                        created_at,
                        updated_at
                    FROM officers 
                    WHERE id = %s
                """
                cursor.execute(query, (officer_id,))
                return cursor.fetchone()
    
    @staticmethod
    def create_officer(officer_data):
        """
        Create a new officer.
        
        Args:
            officer_data (dict): Officer data to insert
            
        Returns:
            str: ID of newly created officer
            
        Raises:
            ValueError: If officer with same staff_id already exists
        """
        officer_id = str(uuid.uuid4())
        
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Check if officer with same staff_id already exists
                check_query = "SELECT id, staff_name FROM officers WHERE staff_id = %s"
                cursor.execute(check_query, (officer_data.get('staff_id'),))
                existing_officer = cursor.fetchone()
                
                if existing_officer:
                    raise ValueError(
                        f"Officer with Staff ID '{officer_data.get('staff_id')}' already exists "
                        f"({existing_officer.get('staff_name', 'Unknown')})"
                    )
                
                query = """
                    INSERT INTO officers 
                    (id, staff_id, staff_name, staff_designation, staff_nature_of_work, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    officer_id,
                    officer_data.get('staff_id'),
                    officer_data.get('staff_name'),
                    officer_data.get('staff_designation'),
                    officer_data.get('staff_nature_of_work', ''),
                    officer_data.get('status', 'active')
                ))
                conn.commit()
                return officer_id
    
    @staticmethod
    def update_officer(officer_id, officer_data):
        """
        Update an existing officer.
        
        Args:
            officer_id (str): Officer ID to update
            officer_data (dict): Officer data to update
            
        Returns:
            bool: True if updated, False if not found
        """
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Build dynamic update query based on provided fields
                update_fields = []
                values = []
                
                if 'staff_id' in officer_data:
                    update_fields.append('staff_id = %s')
                    values.append(officer_data['staff_id'])
                if 'staff_name' in officer_data:
                    update_fields.append('staff_name = %s')
                    values.append(officer_data['staff_name'])
                if 'staff_designation' in officer_data:
                    update_fields.append('staff_designation = %s')
                    values.append(officer_data['staff_designation'])
                if 'staff_nature_of_work' in officer_data:
                    update_fields.append('staff_nature_of_work = %s')
                    values.append(officer_data['staff_nature_of_work'])
                if 'status' in officer_data:
                    update_fields.append('status = %s')
                    values.append(officer_data['status'])
                
                if not update_fields:
                    return False
                
                values.append(officer_id)
                query = f"UPDATE officers SET {', '.join(update_fields)} WHERE id = %s"
                
                cursor.execute(query, tuple(values))
                conn.commit()
                return cursor.rowcount > 0
    
    @staticmethod
    def delete_officer(officer_id):
        """
        Delete an officer.
        
        Args:
            officer_id (str): Officer ID to delete
            
        Returns:
            bool: True if deleted, False if not found
        """
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = "DELETE FROM officers WHERE id = %s"
                cursor.execute(query, (officer_id,))
                conn.commit()
                return cursor.rowcount > 0