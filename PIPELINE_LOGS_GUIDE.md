# 📊 GitHub Actions Pipeline Logs Guide

## 🔍 How to Check Pipeline Logs

### **Method 1: GitHub Web Interface (Recommended)**

#### **Step 1: Go to Actions Tab**
1. Navigate to: https://github.com/Sanjeewa1995/M-AUTO-ZONE-API
2. Click on **"Actions"** tab (top navigation)
3. You'll see a list of workflow runs

#### **Step 2: Select Latest Workflow Run**
Look for the most recent run with message:
- `"deploy: Trigger deployment with GitHub secrets configured"`
- Click on the workflow run

#### **Step 3: View Job Details**
1. Click on **"Deploy to EC2"** job
2. You'll see all the deployment steps:
   - ✅ Checkout code
   - ✅ Setup Python
   - ✅ Install dependencies
   - ✅ Run tests
   - ✅ Create deployment package
   - ✅ Deploy to EC2
   - ✅ Extract and deploy
   - ✅ Start Docker container
   - ✅ Health check

#### **Step 4: Check Individual Step Logs**
1. Click on any step to expand it
2. View detailed logs for that step
3. Look for error messages in red

### **Method 2: Real-time Monitoring**

#### **Check Deployment Status**
```bash
# Check if GitHub Actions is running
curl -s https://api.github.com/repos/Sanjeewa1995/M-AUTO-ZONE-API/actions/runs | jq '.workflow_runs[0].status'
```

#### **Monitor EC2 Status**
```bash
# Check container status
ssh -i vehicle-parts-key.pem ec2-user@3.107.165.131 "docker ps"

# Check container logs
ssh -i vehicle-parts-key.pem ec2-user@3.107.165.131 "docker logs vehicle-parts-api --tail 20"

# Check if new code is deployed
ssh -i vehicle-parts-key.pem ec2-user@3.107.165.131 "ls -la /home/ec2-user/vehicle-parts-api/"
```

### **Method 3: Common Issues & Solutions**

#### **❌ Deployment Failed - Check These:**

1. **SSH Connection Failed**
   - Error: `Permission denied (publickey)`
   - Solution: Verify `EC2_SSH_KEY` secret is correct

2. **Container Build Failed**
   - Error: `Docker build failed`
   - Solution: Check Dockerfile and requirements.txt

3. **Database Connection Failed**
   - Error: `Database connection error`
   - Solution: Verify RDS credentials

4. **Port Already in Use**
   - Error: `Port 8000 already in use`
   - Solution: Stop existing containers first

#### **✅ Success Indicators:**

1. **GitHub Actions**
   - ✅ All steps show green checkmarks
   - ✅ "Deploy to EC2" job completed successfully
   - ✅ No error messages in logs

2. **EC2 Deployment**
   - ✅ New container created (not 46 hours old)
   - ✅ API responding at http://3.107.165.131:8000
   - ✅ OTP endpoints working

### **Method 4: Manual Deployment Check**

If GitHub Actions fails, you can deploy manually:

```bash
# Run manual deployment
./manual_deploy.sh

# Or SSH and update manually
ssh -i vehicle-parts-key.pem ec2-user@3.107.165.131
cd /home/ec2-user/vehicle-parts-api
git pull origin main
docker restart vehicle-parts-api
```

## 🎯 **Quick Status Check Commands**

### **Check API Status**
```bash
# Test basic API
curl http://3.107.165.131:8000/api/v1/auth/register/ -X POST -H "Content-Type: application/json" -d '{"test": "test"}'

# Test OTP endpoint
curl -X POST http://3.107.165.131:8000/api/v1/auth/password-reset/ \
  -H "Content-Type: application/json" \
  -d '{"email": "malakasanjeewa1995@gmail.com"}'
```

### **Check Container Age**
```bash
# See when container was created
ssh -i vehicle-parts-key.pem ec2-user@3.107.165.131 "docker inspect vehicle-parts-api | grep Created"
```

## 📱 **Real-time Monitoring URLs**

- **GitHub Actions**: https://github.com/Sanjeewa1995/M-AUTO-ZONE-API/actions
- **API Health**: http://3.107.165.131:8000/api/v1/auth/register/
- **OTP Test**: http://3.107.165.131:8000/api/v1/auth/password-reset/

## 🚨 **Troubleshooting Steps**

1. **Check GitHub Actions logs first**
2. **Verify secrets are configured correctly**
3. **Check EC2 container status**
4. **Test API endpoints**
5. **Run manual deployment if needed**

## 🎉 **Success Criteria**

- ✅ GitHub Actions shows all green checkmarks
- ✅ EC2 container is recently created (not 46 hours old)
- ✅ API responds to requests
- ✅ OTP endpoints work without 500 errors
