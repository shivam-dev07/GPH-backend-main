-- ============================================================================
-- JWT Authentication Migration
-- Adds required fields and tables for JWT-based authentication
-- ============================================================================

-- Add phone_number column to officers table (if it doesn't exist)
ALTER TABLE officers 
ADD COLUMN IF NOT EXISTS phone_number VARCHAR(20) UNIQUE,
ADD INDEX IF NOT EXISTS idx_phone_number (phone_number);

-- ============================================================================
-- OTP_CODES TABLE
-- Stores one-time passwords for phone number verification
-- ============================================================================
CREATE TABLE IF NOT EXISTS otp_codes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    phone_number VARCHAR(20) NOT NULL,
    otp_code VARCHAR(10) NOT NULL,
    expiration_time DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_phone_number (phone_number),
    INDEX idx_expiration (expiration_time),
    INDEX idx_phone_otp (phone_number, otp_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- Optional: Add refresh_tokens table for advanced JWT implementation
-- ============================================================================
CREATE TABLE IF NOT EXISTS refresh_tokens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    officer_id VARCHAR(50) NOT NULL,
    token VARCHAR(500) NOT NULL UNIQUE,
    expires_at DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    revoked BOOLEAN DEFAULT FALSE,
    revoked_at DATETIME,
    FOREIGN KEY (officer_id) REFERENCES officers(id) ON DELETE CASCADE,
    INDEX idx_officer_id (officer_id),
    INDEX idx_token (token),
    INDEX idx_expires_at (expires_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- Optional: Add JWT blacklist table for token revocation
-- ============================================================================
CREATE TABLE IF NOT EXISTS jwt_blacklist (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jti VARCHAR(255) NOT NULL UNIQUE COMMENT 'JWT ID - unique identifier for each token',
    officer_id VARCHAR(50) NOT NULL,
    token_type ENUM('access', 'refresh') DEFAULT 'access',
    revoked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME NOT NULL,
    reason VARCHAR(255),
    FOREIGN KEY (officer_id) REFERENCES officers(id) ON DELETE CASCADE,
    INDEX idx_jti (jti),
    INDEX idx_officer_id (officer_id),
    INDEX idx_expires_at (expires_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- Clean up expired OTPs (run this periodically via a cron job)
-- ============================================================================
-- DELETE FROM otp_codes WHERE expiration_time < NOW();

-- ============================================================================
-- Clean up expired blacklisted tokens (run this periodically via a cron job)
-- ============================================================================
-- DELETE FROM jwt_blacklist WHERE expires_at < NOW();

-- ============================================================================
-- Sample Data (Optional - for testing)
-- ============================================================================
-- Update existing officers with sample phone numbers (REMOVE IN PRODUCTION)
-- UPDATE officers SET phone_number = CONCAT('9', LPAD(id, 9, '0')) WHERE phone_number IS NULL LIMIT 10;
