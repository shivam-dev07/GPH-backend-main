-- ============================================================================
-- Goa Police Patrol Management System - MySQL Schema
-- Migration from Firebase to MySQL
-- ============================================================================

-- Disable foreign key checks to allow clean table drops
SET FOREIGN_KEY_CHECKS = 0;

-- Drop existing tables (in reverse dependency order)
DROP TABLE IF EXISTS compliance;
DROP TABLE IF EXISTS activities;
DROP TABLE IF EXISTS check_ins;
DROP TABLE IF EXISTS duty_compliance;
DROP TABLE IF EXISTS duty_officers;
DROP TABLE IF EXISTS live_locations;
DROP TABLE IF EXISTS notifications;
DROP TABLE IF EXISTS officer_credits;
DROP TABLE IF EXISTS mobile_patrols;
DROP TABLE IF EXISTS duties;
DROP TABLE IF EXISTS duty_locations;
DROP TABLE IF EXISTS vehicles;
DROP TABLE IF EXISTS officers;

-- ============================================================================
-- OFFICERS TABLE
-- ============================================================================
CREATE TABLE officers (
    id VARCHAR(50) PRIMARY KEY,
    staff_id VARCHAR(50) UNIQUE NOT NULL,
    staff_name VARCHAR(255) NOT NULL,
    staff_designation VARCHAR(255),
    staff_nature_of_work VARCHAR(255),
    status ENUM('active', 'inactive', 'on-duty') DEFAULT 'active',
    profilepic TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_staff_id (staff_id),
    INDEX idx_status (status),
    INDEX idx_staff_name (staff_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- VEHICLES TABLE
-- ============================================================================
CREATE TABLE vehicles (
    id VARCHAR(50) PRIMARY KEY,
    vehicle_name VARCHAR(255) NOT NULL,
    vehicle_number VARCHAR(50) NOT NULL,
    status ENUM('available', 'assigned', 'maintenance') DEFAULT 'available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_vehicle_number (vehicle_number),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- DUTY LOCATIONS TABLE
-- ============================================================================
CREATE TABLE duty_locations (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    center_lat DECIMAL(10, 7) NOT NULL,
    center_lng DECIMAL(10, 7) NOT NULL,
    radius INT NOT NULL,
    polygon JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_location (center_lat, center_lng)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- DUTIES TABLE
-- ============================================================================
CREATE TABLE duties (
    id VARCHAR(50) PRIMARY KEY,
    type ENUM('patrol', 'naka', 'checkpost') NOT NULL,
    location_polygon JSON NOT NULL,
    location_radius INT,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    status ENUM('incomplete', 'assigned', 'active', 'complete', 'completed', 'missed') DEFAULT 'incomplete',
    assigned_at DATETIME NOT NULL,
    comments TEXT,
    check_in_time DATETIME,
    check_out_time DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_updated DATETIME,
    INDEX idx_status (status),
    INDEX idx_type (type),
    INDEX idx_start_time (start_time),
    INDEX idx_end_time (end_time),
    INDEX idx_assigned_at (assigned_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- DUTY_OFFICERS (Junction Table for Many-to-Many)
-- ============================================================================
CREATE TABLE duty_officers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    duty_id VARCHAR(50) NOT NULL,
    officer_id VARCHAR(50) NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (duty_id) REFERENCES duties(id) ON DELETE CASCADE,
    FOREIGN KEY (officer_id) REFERENCES officers(id) ON DELETE CASCADE,
    UNIQUE KEY unique_duty_officer (duty_id, officer_id),
    INDEX idx_duty_id (duty_id),
    INDEX idx_officer_id (officer_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- DUTY_VEHICLES (Junction Table for Many-to-Many)
-- ============================================================================
CREATE TABLE duty_vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    duty_id VARCHAR(50) NOT NULL,
    vehicle_id VARCHAR(50) NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (duty_id) REFERENCES duties(id) ON DELETE CASCADE,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE,
    UNIQUE KEY unique_duty_vehicle (duty_id, vehicle_id),
    INDEX idx_duty_id (duty_id),
    INDEX idx_vehicle_id (vehicle_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- LIVE LOCATIONS TABLE
-- ============================================================================
CREATE TABLE live_locations (
    id VARCHAR(50) PRIMARY KEY,
    officer_id VARCHAR(50) NOT NULL,
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    speed DECIMAL(8, 2),
    altitude DECIMAL(8, 2),
    heading DECIMAL(6, 2),
    accuracy DECIMAL(8, 2),
    timestamp DATETIME,
    local_time VARCHAR(50),
    current_location JSON,
    location_history JSON,
    locations JSON,
    total_points INT DEFAULT 0,
    tracking_started DATETIME,
    last_seen DATETIME,
    last_updated DATETIME,
    status ENUM('online', 'offline', 'active', 'inactive') DEFAULT 'offline',
    is_active BOOLEAN DEFAULT true,
    FOREIGN KEY (officer_id) REFERENCES officers(id) ON DELETE CASCADE,
    INDEX idx_officer_id (officer_id),
    INDEX idx_status (status),
    INDEX idx_location (latitude, longitude),
    INDEX idx_last_updated (last_updated)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- NOTIFICATIONS TABLE
-- ============================================================================
CREATE TABLE notifications (
    id VARCHAR(50) PRIMARY KEY,
    officer_id VARCHAR(50),
    type ENUM('duty', 'alert', 'message', 'system') DEFAULT 'duty',
    title VARCHAR(255) NOT NULL,
    body TEXT,
    message TEXT,
    data JSON,
    duty_type VARCHAR(50),
    duty_id VARCHAR(50),
    location_polygon JSON,
    vehicle_ids JSON,
    start_time DATETIME,
    end_time DATETIME,
    status VARCHAR(50),
    comments TEXT,
    `read` BOOLEAN DEFAULT false,
    read_at DATETIME,
    deleted BOOLEAN DEFAULT false,
    deleted_at DATETIME,
    sent_at DATETIME,
    timestamp DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (officer_id) REFERENCES officers(id) ON DELETE CASCADE,
    INDEX idx_officer_id (officer_id),
    INDEX idx_type (type),
    INDEX idx_read (`read`),
    INDEX idx_deleted (deleted),
    INDEX idx_sent_at (sent_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- ACTIVITIES TABLE
-- ============================================================================
CREATE TABLE activities (
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
    FOREIGN KEY (officer_id) REFERENCES officers(id) ON DELETE CASCADE,
    FOREIGN KEY (duty_id) REFERENCES duties(id) ON DELETE CASCADE,
    INDEX idx_officer_id (officer_id),
    INDEX idx_duty_id (duty_id),
    INDEX idx_type (type),
    INDEX idx_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- CHECK-INS TABLE
-- ============================================================================
CREATE TABLE check_ins (
    id VARCHAR(50) PRIMARY KEY,
    officer_id VARCHAR(50),
    officer_uid VARCHAR(50),
    duty_id VARCHAR(50) NOT NULL,
    check_in_type ENUM('start', 'end', 'checkpoint') NOT NULL,
    location JSON,
    selfie_image_url TEXT,
    device_info JSON,
    verified BOOLEAN DEFAULT false,
    verification_method ENUM('geolocation', 'manual', 'qr-code') DEFAULT 'geolocation',
    compliance_score INT DEFAULT 0,
    timestamp DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (officer_id) REFERENCES officers(id) ON DELETE CASCADE,
    FOREIGN KEY (duty_id) REFERENCES duties(id) ON DELETE CASCADE,
    INDEX idx_officer_id (officer_id),
    INDEX idx_duty_id (duty_id),
    INDEX idx_check_in_type (check_in_type),
    INDEX idx_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- COMPLIANCE TABLE
-- ============================================================================
CREATE TABLE compliance (
    id VARCHAR(50) PRIMARY KEY,
    duty_id VARCHAR(50),
    officer_id VARCHAR(50),
    officer_uid VARCHAR(50),
    officer_name VARCHAR(255),
    action ENUM('check-in', 'check-out', 'patrol-update', 'geofence-violation', 'incident-report') NOT NULL,
    location JSON,
    timestamp DATETIME NOT NULL,
    details TEXT,
    photo_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (duty_id) REFERENCES duties(id) ON DELETE CASCADE,
    FOREIGN KEY (officer_id) REFERENCES officers(id) ON DELETE CASCADE,
    INDEX idx_duty_id (duty_id),
    INDEX idx_officer_id (officer_id),
    INDEX idx_action (action),
    INDEX idx_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- DUTY COMPLIANCE TABLE
-- ============================================================================
CREATE TABLE duty_compliance (
    id VARCHAR(50) PRIMARY KEY,
    duty_id VARCHAR(50) NOT NULL,
    officer_id VARCHAR(50),
    officer_uid VARCHAR(50),
    total_checkpoints INT DEFAULT 0,
    completed_checkpoints INT DEFAULT 0,
    missed_checkpoints INT DEFAULT 0,
    overall_score INT DEFAULT 0,
    violations INT DEFAULT 0,
    on_time_percentage INT DEFAULT 0,
    last_updated DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (duty_id) REFERENCES duties(id) ON DELETE CASCADE,
    FOREIGN KEY (officer_id) REFERENCES officers(id) ON DELETE CASCADE,
    INDEX idx_duty_id (duty_id),
    INDEX idx_officer_id (officer_id),
    INDEX idx_overall_score (overall_score)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- OFFICER CREDITS TABLE
-- ============================================================================
CREATE TABLE officer_credits (
    id VARCHAR(50) PRIMARY KEY,
    officer_id VARCHAR(50) NOT NULL,
    total_credits INT DEFAULT 0,
    lifetime_credits INT DEFAULT 0,
    current_tier ENUM('Bronze', 'Silver', 'Gold', 'Platinum') DEFAULT 'Bronze',
    badges JSON,
    performance_metrics JSON,
    last_updated DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (officer_id) REFERENCES officers(id) ON DELETE CASCADE,
    INDEX idx_officer_id (officer_id),
    INDEX idx_current_tier (current_tier),
    INDEX idx_total_credits (total_credits)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- MOBILE PATROLS TABLE
-- ============================================================================
CREATE TABLE mobile_patrols (
    id VARCHAR(50) PRIMARY KEY,
    vehicle_name VARCHAR(255) NOT NULL,
    vehicle_number VARCHAR(50) NOT NULL,
    driver_id VARCHAR(50),
    driver_name VARCHAR(255),
    incharge_officer_id VARCHAR(50),
    incharge_officer_name VARCHAR(255),
    path_start JSON,
    path_end JSON,
    status ENUM('on_duty', 'off_duty', 'maintenance') DEFAULT 'off_duty',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (driver_id) REFERENCES officers(id) ON DELETE SET NULL,
    FOREIGN KEY (incharge_officer_id) REFERENCES officers(id) ON DELETE SET NULL,
    INDEX idx_vehicle_number (vehicle_number),
    INDEX idx_status (status),
    INDEX idx_driver_id (driver_id),
    INDEX idx_incharge_officer_id (incharge_officer_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- Create Views for Common Queries
-- ============================================================================

-- View for active duties with officer details
CREATE OR REPLACE VIEW active_duties_view AS
SELECT 
    d.id,
    d.type,
    d.start_time,
    d.end_time,
    d.status,
    GROUP_CONCAT(DISTINCT o.staff_name ORDER BY o.staff_name SEPARATOR ', ') as officer_names,
    GROUP_CONCAT(DISTINCT o.id ORDER BY o.id SEPARATOR ',') as officer_ids,
    d.location_polygon,
    d.location_radius,
    d.assigned_at
FROM duties d
LEFT JOIN duty_officers do ON d.id = do.duty_id
LEFT JOIN officers o ON do.officer_id = o.id
WHERE d.status IN ('active', 'assigned')
GROUP BY d.id, d.type, d.start_time, d.end_time, d.status, d.location_polygon, d.location_radius, d.assigned_at;

-- View for recent activities with officer details
CREATE OR REPLACE VIEW recent_activities_view AS
SELECT 
    a.id,
    a.type,
    a.title,
    a.description,
    a.location,
    a.timestamp,
    o.staff_name as officer_name,
    o.staff_id as officer_staff_id,
    a.duty_id
FROM activities a
LEFT JOIN officers o ON a.officer_id = o.id
ORDER BY a.timestamp DESC
LIMIT 100;

-- ============================================================================
-- Sample Data Verification Queries
-- ============================================================================

-- Count records in each table
-- SELECT 'officers' as table_name, COUNT(*) as count FROM officers
-- UNION ALL SELECT 'vehicles', COUNT(*) FROM vehicles
-- UNION ALL SELECT 'duties', COUNT(*) FROM duties
-- UNION ALL SELECT 'duty_officers', COUNT(*) FROM duty_officers
-- UNION ALL SELECT 'activities', COUNT(*) FROM activities
-- UNION ALL SELECT 'check_ins', COUNT(*) FROM check_ins
-- UNION ALL SELECT 'compliance', COUNT(*) FROM compliance
-- UNION ALL SELECT 'notifications', COUNT(*) FROM notifications
-- UNION ALL SELECT 'live_locations', COUNT(*) FROM live_locations;

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;
