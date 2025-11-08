#!/bin/bash
# Run migrations on EC2 instance
# Usage: ./run-migrations-ec2.sh

export AWS_PROFILE="vehicle_parts"

echo "🔄 Running migrations on EC2 instance..."

# Command to run migrations inside the Docker container
ssh -i ~/.ssh/vehicle-parts-key.pem -o StrictHostKeyChecking=no ec2-user@3.25.146.196 << 'EOF'
  echo "📦 Running migrations inside Docker container..."
  docker exec vehicle-parts-api python manage.py migrate --noinput
  echo "✅ Migrations completed!"
  echo ""
  echo "📋 Checking container logs..."
  docker logs vehicle-parts-api --tail 10
EOF

echo "✅ Done!"

