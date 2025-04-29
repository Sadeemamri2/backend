-- SQL script to create PostgreSQL database and user for Hudoorr project

-- 1. Create a new database
CREATE DATABASE hudoorr_db;

-- 2. Create a new database user and set password
CREATE USER hudoorr_user WITH PASSWORD 'YourStrongPassword';

-- 3. Grant all privileges on the database to the new user
GRANT ALL PRIVILEGES ON DATABASE hudoorr_db TO hudoorr_user;

-- 4. (Optional) Make the new user owner of the public schema
\c hudoorr_db;
ALTER SCHEMA public OWNER TO hudoorr_user;
