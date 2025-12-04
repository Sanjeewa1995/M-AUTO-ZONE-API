#!/bin/bash

# Django Application Deployment Script
# This script deploys the Django application to the server

set -e  # Exit on any error

APP_DIR="/var/www/vehicle-parts-api"
VENV_DIR="$APP_DIR/venv"
USER=$(whoami)

echo "========================================="
echo "Django Application Deployment"
echo "========================================="

# Navigate to application directory
cd $APP_DIR

# Check if virtual environment exists, create if not
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv $VENV_DIR
fi

# Activate virtual environment
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install/upgrade dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Create superuser if it doesn't exist (optional, comment out if not needed)
# echo "Creating superuser (if needed)..."
# python manage.py shell <<EOF
# from authentication.models import User
# if not User.objects.filter(is_superuser=True).exists():
#     User.objects.create_superuser('admin', 'admin@example.com', 'changeme123!')
# EOF

# Set proper permissions
echo "Setting file permissions..."
sudo chown -R $USER:$USER $APP_DIR
sudo chmod -R 755 $APP_DIR
sudo chmod -R 775 $APP_DIR/media
sudo chmod -R 775 $APP_DIR/staticfiles

# Restart services
echo "Restarting services..."
sudo systemctl restart vehicle-parts-api
sudo systemctl restart nginx

# Check service status
echo "Checking service status..."
sudo systemctl status vehicle-parts-api --no-pager -l

echo "========================================="
echo "Deployment completed!"
echo "========================================="
echo "Your Django application should now be running."
echo "Check the status with: sudo systemctl status vehicle-parts-api"

