-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS ALX_prodev;

-- Use the database
USE ALX_prodev;

-- Create user_data table
CREATE TABLE IF NOT EXISTS user_data (
    user_id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    age DECIMAL(3,0) NOT NULL,
    INDEX idx_user_id (user_id)
);

-- Create index on email for faster lookups
CREATE INDEX idx_email ON user_data(email);
