CREATE DATABASE IF NOT EXISTS room_reservation
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE room_reservation;

CREATE TABLE IF NOT EXISTS room_reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reservation_no VARCHAR(20) NOT NULL UNIQUE,
    requester_name VARCHAR(150) NOT NULL,
    department VARCHAR(100) NOT NULL,
    room_name VARCHAR(100) NOT NULL,
    participants INT UNSIGNED NOT NULL,
    reservation_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    purpose VARCHAR(255) NOT NULL,
    status VARCHAR(20) NOT NULL,
    encoded_by VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
