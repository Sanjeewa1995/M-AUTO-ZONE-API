#!/bin/bash

# Vehicle Parts API - EC2 Deployment Script for CodePipeline
# This script is executed on EC2 instance during deployment

echo "🚀 Starting EC2 Deployment via CodePipeline..."

# Set environment variables
export SECRET_KEY="your-production-secret-key-here"
export DEBUG="False"
export ALLOWED_HOSTS="3.107.165.131,localhost,127.0.0.1"
export DB_HOST="vehicle-parts-db.c5m26imqm4kv.ap-southeast-2.rds.amazonaws.com"
export DB_PORT="3306"
export DB_USER="admin"
export DB_PASSWORD="VehicleParts123!"
export DB_NAME="vehicle_parts"
export EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend"
export DEFAULT_FROM_EMAIL="noreply@vehicleparts.com"
export CORS_ALLOWED_ORIGINS="http://localhost:3000,http://127.0.0.1:3000,http://3.107.165.131:8000"

# Navigate to deployment directory
cd /home/ec2-user/vehicle-parts-api

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker stop $(docker ps -q) 2>/dev/null || true
docker rm $(docker ps -aq) 2>/dev/null || true

# Install dependencies
echo "📥 Installing dependencies..."
pip3 install -r requirements.txt

# Run migrations
echo "🔄 Running database migrations..."
python3 manage.py makemigrations
python3 manage.py migrate

# Build and run Docker container
echo "🐳 Building and running Docker container..."
docker build -t vehicle-parts-api .
docker run -d --name vehicle-parts-api -p 8000:8000 \
  -e SECRET_KEY="$SECRET_KEY" \
  -e DEBUG="$DEBUG" \
  -e ALLOWED_HOSTS="$ALLOWED_HOSTS" \
  -e DB_HOST="$DB_HOST" \
  -e DB_PORT="$DB_PORT" \
  -e DB_USER="$DB_USER" \
  -e DB_PASSWORD="$DB_PASSWORD" \
  -e DB_NAME="$DB_NAME" \
  -e EMAIL_BACKEND="$EMAIL_BACKEND" \
  -e DEFAULT_FROM_EMAIL="$DEFAULT_FROM_EMAIL" \
  -e CORS_ALLOWED_ORIGINS="$CORS_ALLOWED_ORIGINS" \
  vehicle-parts-api

# Wait for container to start
echo "⏳ Waiting for container to start..."
sleep 15

# Check container status
echo "🔍 Checking container status..."
docker ps

# Test the API
echo "🧪 Testing API..."
curl -s http://localhost:8000/api/v1/auth/health/ || echo "Health check failed"

echo "✅ Deployment completed successfully!"
echo "🌐 API is available at: http://3.107.165.131:8000"
