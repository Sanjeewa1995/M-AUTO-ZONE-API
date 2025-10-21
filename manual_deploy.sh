#!/bin/bash

# Manual Deployment Script for Vehicle Parts API
# This script manually deploys the latest code to EC2

echo "🚀 Starting Manual Deployment to EC2..."

# Configuration
EC2_HOST="3.107.165.131"
EC2_USER="ec2-user"
SSH_KEY="./vehicle-parts-key.pem"

# Check if SSH key exists
if [ ! -f "$SSH_KEY" ]; then
    echo "❌ SSH key not found: $SSH_KEY"
    exit 1
fi

# Set proper permissions for SSH key
chmod 400 "$SSH_KEY"

echo "📦 Creating deployment package..."

# Create a clean deployment package
tar -czf ../vehicle-parts-api-manual.tar.gz \
  --exclude='venv' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='.git' \
  --exclude='.env*' \
  --exclude='*.log' \
  --exclude='staticfiles' \
  --exclude='media' \
  --exclude='*.tar.gz' \
  --exclude='manual_deploy.sh' \
  .

echo "📤 Uploading to EC2..."

# Upload the package to EC2
scp -i "$SSH_KEY" ../vehicle-parts-api-manual.tar.gz "$EC2_USER@$EC2_HOST:/home/ec2-user/"

echo "🔧 Deploying on EC2..."

# Deploy on EC2
ssh -i "$SSH_KEY" "$EC2_USER@$EC2_HOST" << 'EOF'
cd /home/ec2-user

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker stop $(docker ps -q) 2>/dev/null || true
docker rm $(docker ps -aq) 2>/dev/null || true

# Remove old deployment
echo "🗑️ Removing old deployment..."
rm -rf vehicle-parts-api

# Extract new deployment
echo "📦 Extracting new deployment..."
tar -xzf vehicle-parts-api-manual.tar.gz
mv vehicle-parts-api-manual vehicle-parts-api
cd vehicle-parts-api

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
  -e SECRET_KEY="your-production-secret-key-here" \
  -e DEBUG="False" \
  -e ALLOWED_HOSTS="3.107.165.131,localhost,127.0.0.1" \
  -e DB_HOST="vehicle-parts-db.c5m26imqm4kv.ap-southeast-2.rds.amazonaws.com" \
  -e DB_PORT="3306" \
  -e DB_USER="admin" \
  -e DB_PASSWORD="VehicleParts123!" \
  -e DB_NAME="vehicle_parts" \
  -e EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend" \
  -e DEFAULT_FROM_EMAIL="noreply@vehicleparts.com" \
  -e CORS_ALLOWED_ORIGINS="http://localhost:3000,http://127.0.0.1:3000,http://3.107.165.131:8000" \
  vehicle-parts-api

# Wait for container to start
echo "⏳ Waiting for container to start..."
sleep 15

# Check container status
echo "🔍 Checking container status..."
docker ps

# Test the API
echo "🧪 Testing API..."
curl -s http://localhost:8000/api/v1/auth/register/ -X POST -H "Content-Type: application/json" -d '{"test": "test"}' || echo "API test failed"

echo "✅ Manual deployment completed!"
echo "🌐 API is available at: http://3.107.165.131:8000"
EOF

echo "🎉 Manual deployment completed successfully!"
echo "🌐 Your API is now available at: http://3.107.165.131:8000"
