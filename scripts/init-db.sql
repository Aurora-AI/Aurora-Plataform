-- init-db.sql - Database initialization script for Aurora-Plataform
-- This script runs when PostgreSQL container is first created

-- Create additional databases if needed
-- CREATE DATABASE aurora_crawler;

-- Create extensions that might be needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Set timezone
SET timezone = 'UTC';

-- Create initial schema (if not using Alembic migrations)
-- Tables will be created by Aurora-Core's Alembic migrations

-- Optional: Create read-only user for analytics
-- CREATE USER aurora_readonly WITH PASSWORD 'readonly_password';
-- GRANT CONNECT ON DATABASE aurora_core TO aurora_readonly;
-- GRANT USAGE ON SCHEMA public TO aurora_readonly;
-- GRANT SELECT ON ALL TABLES IN SCHEMA public TO aurora_readonly;
-- ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO aurora_readonly;

-- Log initialization
SELECT 'Aurora-Plataform database initialized successfully' as message;