#!/bin/bash

# DigitalOcean Droplet Setup Script for Django + MySQL
# This script sets up a fresh Ubuntu server with all necessary components

set -e  # Exit on any error

echo "========================================="
echo "DigitalOcean Droplet Setup Script"
echo "========================================="

# Update system packages
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install essential packages
echo "Installing essential packages..."
sudo apt-get install -y \
    python3 \
    python3-venv \
    python3-pip \
    mysql-server \
    mysql-client \
    nginx \
    git \
    curl \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    supervisor \
    certbot \
    python3-certbot-nginx \
    ufw \
    htop

# Start and enable MySQL
echo "Configuring MySQL..."
sudo systemctl start mysql
sudo systemctl enable mysql

# Secure MySQL installation (non-interactive)
echo "Securing MySQL installation..."
MYSQL_ROOT_PASSWORD="${MYSQL_ROOT_PASSWORD:-TempRootPass123!}"

# Try to set root password (may fail if already set, that's okay)
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '${MYSQL_ROOT_PASSWORD}';" 2>/dev/null || \
sudo mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "SELECT 1;" 2>/dev/null || \
echo "MySQL root password may already be set, continuing..."

# Clean up MySQL
sudo mysql -u root -p"${MYSQL_ROOT_PASSWORD}" <<EOF 2>/dev/null || sudo mysql <<EOF
DELETE FROM mysql.user WHERE User='';
DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');
DROP DATABASE IF EXISTS test;
DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';
FLUSH PRIVILEGES;
EOF

# Create application directory
echo "Creating application directory..."
sudo mkdir -p /var/www/vehicle-parts-api
sudo chown -R $USER:$USER /var/www/vehicle-parts-api

# Configure firewall
echo "Configuring firewall..."
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw --force enable

# Create log directories
echo "Creating log directories..."
sudo mkdir -p /var/log/vehicle-parts-api
sudo chown -R $USER:$USER /var/log/vehicle-parts-api

echo "========================================="
echo "Server setup completed!"
echo "========================================="
echo "Next steps:"
echo "1. Clone your repository to /var/www/vehicle-parts-api"
echo "2. Run the database setup script: ./deploy/setup-database.sh"
echo "3. Configure your .env file"
echo "4. Run the deployment script: ./deploy/deploy.sh"

