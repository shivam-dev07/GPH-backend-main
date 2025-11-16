"""
Seed Activities Script
Creates sample activity logs for testing
"""

from models.db import get_connection
from datetime import datetime, timedelta
import uuid

def seed_activities():
    """Create sample activities"""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            # Get some officer IDs and duty IDs
            cursor.execute("SELECT id, staff_id FROM officers LIMIT 5")
            officers = cursor.fetchall()
            
            cursor.execute("SELECT id FROM duties LIMIT 5")
            duties = cursor.fetchall()
            
            if not officers or not duties:
                print("No officers or duties found. Please create them first.")
                return
            
            # Create sample activities
            activities = []
            base_time = datetime.now() - timedelta(hours=2)
            
            activity_types = [
                ('check-in', 'Officer checked in for patrol duty', 'Started patrol at checkpoint'),
                ('patrol-update', 'Patrol route update', 'Completed checkpoint 1 of 3'),
                ('check-out', 'Officer checked out', 'Completed patrol duty'),
                ('incident-report', 'Minor incident reported', 'Suspicious activity near market area'),
                ('geofence-violation', 'Geofence boundary crossed', 'Officer moved outside designated patrol area')
            ]
            
            for i, (act_type, title, desc) in enumerate(activity_types):
                officer = officers[i % len(officers)]
                duty = duties[i % len(duties)]
                
                activity_id = str(uuid.uuid4())
                timestamp = base_time + timedelta(minutes=i*20)
                
                activities.append((
                    activity_id,
                    officer['id'],
                    officer['staff_id'],
                    duty['id'],
                    act_type,
                    title,
                    desc,
                    'Patrol Area, Goa',
                    timestamp
                ))
            
            # Insert activities
            query = """
                INSERT INTO activities 
                (id, officer_id, officer_uid, duty_id, type, title, description, location, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.executemany(query, activities)
            conn.commit()
            
            print(f"✅ Created {len(activities)} sample activities")
            print("\nSample activities:")
            for act in activities:
                print(f"  - {act[5]} ({act[4]}) at {act[8]}")

if __name__ == '__main__':
    print("Seeding activities...")
    seed_activities()
    print("\nDone! Check the dashboard to see the Recent Activity Logs.")
