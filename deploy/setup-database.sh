#!/bin/bash

# MySQL Database Setup Script
# This script creates the database and user for the Django application

set -e  # Exit on any error

echo "========================================="
echo "MySQL Database Setup"
echo "========================================="

# Load environment variables if .env file exists
if [ -f /var/www/vehicle-parts-api/.env ]; then
    export $(cat /var/www/vehicle-parts-api/.env | grep -v '^#' | xargs)
fi

# Default values
DB_NAME=${DB_NAME:-vehicle_parts}
DB_USER=${DB_USER:-vehicle_parts_user}
DB_PASSWORD=${DB_PASSWORD:-$(openssl rand -base64 32)}
MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD:-TempRootPass123!}

echo "Creating database: $DB_NAME"
echo "Creating user: $DB_USER"

# Create database and user
sudo mysql -u root -p"$MYSQL_ROOT_PASSWORD" <<EOF
CREATE DATABASE IF NOT EXISTS $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASSWORD';
GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';
FLUSH PRIVILEGES;
EOF

echo "========================================="
echo "Database setup completed!"
echo "========================================="
echo "Database Name: $DB_NAME"
echo "Database User: $DB_USER"
echo "Database Password: $DB_PASSWORD"
echo ""
echo "Please save these credentials and update your .env file:"
echo "DB_NAME=$DB_NAME"
echo "DB_USER=$DB_USER"
echo "DB_PASSWORD=$DB_PASSWORD"
echo "DB_HOST=localhost"
echo "DB_PORT=3306"

