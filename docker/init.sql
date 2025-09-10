-- Initial database setup for protocollum development
-- This script runs when the PostgreSQL container starts for the first time

-- Create a sample schema for testing
CREATE SCHEMA IF NOT EXISTS protocollum_schema;

-- Set default search path
ALTER DATABASE protocollum_dev SET search_path TO protocollum_schema,public;

-- Create a sample table for testing schema bindings
CREATE TABLE IF NOT EXISTS protocollum_schema.sample_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some sample data
INSERT INTO protocollum_schema.sample_table (name, email) VALUES 
    ('Sample User 1', 'user1@example.com'),
    ('Sample User 2', 'user2@example.com')
ON CONFLICT (email) DO NOTHING;

-- Create a function to update the updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for automatic updated_at updates
CREATE TRIGGER update_sample_table_updated_at 
    BEFORE UPDATE ON protocollum_schema.sample_table 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();