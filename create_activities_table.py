#!/usr/bin/env python3
"""Create activities table in database"""
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

sql = """
CREATE TABLE IF NOT EXISTS activities (
    id VARCHAR(50) PRIMARY KEY,
    officer_id VARCHAR(50),
    officer_uid VARCHAR(50),
    duty_id VARCHAR(50),
    type ENUM('check-in', 'check-out', 'duty-update', 'patrol-update', 'geofence-violation', 'incident-report') NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    location VARCHAR(255),
    timestamp DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_officer_id (officer_id),
    INDEX idx_duty_id (duty_id),
    INDEX idx_type (type),
    INDEX idx_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

try:
    conn = pymysql.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT', '3306')),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        ssl={'ssl': True}
    )
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    print('✅ Activities table created successfully!')
    cursor.close()
    conn.close()
except Exception as e:
    print(f'❌ Error: {e}')
