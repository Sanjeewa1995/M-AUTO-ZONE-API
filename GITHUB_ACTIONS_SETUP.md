# 🚀 GitHub Actions CI/CD Setup Guide

## Overview
This guide shows you how to set up automatic deployment to EC2 whenever you push to the main branch.

## 🔧 Setup Steps

### 1. Configure GitHub Secrets
Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:
- `EC2_HOST`: `3.107.165.131`
- `EC2_USER`: `ec2-user`
- `EC2_SSH_KEY`: Your private SSH key content (vehicle-parts-key.pem)

### 2. SSH Key Setup
Copy your private key content:
```bash
cat vehicle-parts-key.pem
```
Copy the entire content and paste it as `EC2_SSH_KEY` secret.

### 3. How to Trigger Deployment

#### Method 1: Automatic (Recommended)
```bash
# Make any change to your code
echo "# Test change" >> README.md
git add .
git commit -m "test: trigger deployment"
git push origin main
```

#### Method 2: Manual Trigger
1. Go to GitHub repository
2. Click "Actions" tab
3. Select "Deploy to EC2" workflow
4. Click "Run workflow"
5. Select "main" branch
6. Click "Run workflow"

### 4. Monitor Deployment
- Go to GitHub repository → Actions tab
- Click on the latest workflow run
- Watch the deployment progress in real-time

## 🔄 Deployment Process

When you push to main branch:

1. **Checkout Code** - Downloads your latest code
2. **Setup Python** - Installs Python 3.9
3. **Install Dependencies** - Installs requirements.txt
4. **Run Tests** - Executes Django tests
5. **Create Package** - Creates deployment archive
6. **Deploy to EC2** - Stops old containers, deploys new code
7. **Start Services** - Builds and runs Docker container
8. **Health Check** - Tests API endpoints

## 🎯 Benefits

- ✅ **Automatic Deployment** - No manual intervention needed
- ✅ **Version Control** - Every deployment is tracked
- ✅ **Rollback Capability** - Easy to revert changes
- ✅ **Testing** - Runs tests before deployment
- ✅ **Monitoring** - Real-time deployment logs

## 🔍 Troubleshooting

### If deployment fails:
1. Check GitHub Actions logs
2. Verify EC2 connection
3. Check Docker container status
4. Verify environment variables

### Manual deployment:
```bash
# SSH into EC2
ssh -i vehicle-parts-key.pem ec2-user@3.107.165.131

# Check container status
docker ps

# View logs
docker logs vehicle-parts-api

# Restart container
docker restart vehicle-parts-api
```

## 📱 Testing Your API

After deployment, test your API:
```bash
# Health check
curl http://3.107.165.131:8000/api/v1/auth/health/

# Test OTP endpoint
curl -X POST http://3.107.165.131:8000/api/v1/auth/password-reset/ \
  -H "Content-Type: application/json" \
  -d '{"email": "malakasanjeewa1995@gmail.com"}'
```

## 🎉 Success!

Your API is now automatically deployed whenever you push to the main branch!

**API URL**: http://3.107.165.131:8000
**GitHub Actions**: https://github.com/dewapathi/M-AUTO-ZONE-API/actions
