#!/bin/bash

# Script to upload project files to DigitalOcean droplet
# Usage: ./deploy/upload-to-server.sh

set -e

DROPLET_IP="206.189.137.79"
SSH_KEY="${HOME}/.ssh/id_ed25519_digitalocean"
REMOTE_USER="root"
REMOTE_DIR="/var/www/vehicle-parts-api"

echo "========================================="
echo "Uploading project to DigitalOcean droplet"
echo "========================================="

# Check if rsync is available
if ! command -v rsync &> /dev/null; then
    echo "rsync not found. Installing..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install rsync
        else
            echo "Please install rsync manually or use Homebrew"
            exit 1
        fi
    else
        echo "Please install rsync manually"
        exit 1
    fi
fi

# Create remote directory if it doesn't exist
echo "Creating remote directory..."
ssh -i $SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $REMOTE_USER@$DROPLET_IP "mkdir -p $REMOTE_DIR"

# Upload files using rsync (excludes venv, __pycache__, etc.)
echo "Uploading files..."
rsync -avz --progress \
    -e "ssh -i $SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" \
    --exclude 'venv/' \
    --exclude '__pycache__/' \
    --exclude '*.pyc' \
    --exclude '.git/' \
    --exclude 'media/' \
    --exclude 'staticfiles/' \
    --exclude '.env' \
    --exclude '.env.local' \
    --exclude '*.log' \
    --exclude '.DS_Store' \
    ./ $REMOTE_USER@$DROPLET_IP:$REMOTE_DIR/

echo "========================================="
echo "Upload completed!"
echo "========================================="
echo "Next steps:"
echo "1. SSH into the server: ssh -i $SSH_KEY $REMOTE_USER@$DROPLET_IP"
echo "2. Navigate to: cd $REMOTE_DIR"
echo "3. Run: ./deploy/setup-server.sh"
echo "4. Continue with deployment steps from QUICK_START.md"

