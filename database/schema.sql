-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS pythonproject;
USE pythonproject;

-- Create admins table with secure password storage
CREATE TABLE IF NOT EXISTS admins (
    username VARCHAR(50) PRIMARY KEY,
    password_hash BINARY(60) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP DEFAULT NULL,
    UNIQUE KEY unique_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create base table template for all divisions
CREATE TABLE IF NOT EXISTS base_division (
    enrollment VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    status ENUM('Present', 'Absent') DEFAULT NULL,
    date_day DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    total_present INT DEFAULT 0,
    total_absent INT DEFAULT 0,
    attendance_percentage DECIMAL(5,2) GENERATED ALWAYS AS (
        CASE 
            WHEN (total_present + total_absent) = 0 THEN 0
            ELSE (total_present * 100.0) / (total_present + total_absent)
        END
    ) STORED,
    INDEX idx_date_day (date_day),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create tables for each division based on the template
CREATE TABLE IF NOT EXISTS cea LIKE base_division;
CREATE TABLE IF NOT EXISTS ceb LIKE base_division;
CREATE TABLE IF NOT EXISTS cec LIKE base_division;
CREATE TABLE IF NOT EXISTS ced LIKE base_division;
CREATE TABLE IF NOT EXISTS cee LIKE base_division;

-- Create attendance log table for tracking all attendance records
CREATE TABLE IF NOT EXISTS attendance_log (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    division VARCHAR(10) NOT NULL,
    enrollment VARCHAR(20) NOT NULL,
    status ENUM('Present', 'Absent') NOT NULL,
    date_day DATE NOT NULL,
    marked_by VARCHAR(50) NOT NULL,
    marked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (marked_by) REFERENCES admins(username),
    INDEX idx_division_date (division, date_day),
    INDEX idx_enrollment_date (enrollment, date_day)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create triggers to update attendance statistics
DELIMITER //

CREATE TRIGGER after_attendance_insert 
AFTER INSERT ON attendance_log
FOR EACH ROW
BEGIN
    DECLARE table_name VARCHAR(10);
    SET table_name = NEW.division;
    
    SET @sql = CONCAT('UPDATE ', table_name, 
        ' SET total_present = total_present + ', IF(NEW.status = 'Present', 1, 0),
        ', total_absent = total_absent + ', IF(NEW.status = 'Absent', 1, 0),
        ' WHERE enrollment = "', NEW.enrollment, '"');
    
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //

-- Create stored procedure for generating attendance reports
CREATE PROCEDURE generate_attendance_report(
    IN p_division VARCHAR(10),
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    SELECT 
        d.enrollment,
        d.name,
        d.attendance_percentage,
        COUNT(CASE WHEN al.status = 'Present' THEN 1 END) as present_days,
        COUNT(CASE WHEN al.status = 'Absent' THEN 1 END) as absent_days,
        COUNT(*) as total_days
    FROM attendance_log al
    JOIN cea d ON d.enrollment = al.enrollment
    WHERE al.division = p_division
    AND al.date_day BETWEEN p_start_date AND p_end_date
    GROUP BY d.enrollment, d.name, d.attendance_percentage
    ORDER BY d.enrollment;
END //

DELIMITER ;

-- Create views for easy reporting
CREATE OR REPLACE VIEW daily_attendance_summary AS
SELECT 
    division,
    date_day,
    COUNT(CASE WHEN status = 'Present' THEN 1 END) as present_count,
    COUNT(CASE WHEN status = 'Absent' THEN 1 END) as absent_count,
    COUNT(*) as total_students,
    (COUNT(CASE WHEN status = 'Present' THEN 1 END) * 100.0 / COUNT(*)) as attendance_percentage
FROM attendance_log
GROUP BY division, date_day
ORDER BY date_day DESC;

-- Add sample admin user (password: admin123)
-- Note: In production, use proper password hashing through the application
INSERT IGNORE INTO admins (username, password_hash) 
VALUES ('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY.HHKzGhzS.RS6');

-- Add indexes for better query performance
ALTER TABLE cea ADD INDEX idx_name (name);
ALTER TABLE ceb ADD INDEX idx_name (name);
ALTER TABLE cec ADD INDEX idx_name (name);
ALTER TABLE ced ADD INDEX idx_name (name);
ALTER TABLE cee ADD INDEX idx_name (name);
