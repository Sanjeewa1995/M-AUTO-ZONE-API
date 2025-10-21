# 🔐 GitHub Secrets Configuration Guide

## Step-by-Step Setup

### 1. Go to Your GitHub Repository
- Navigate to: https://github.com/dewapathi/M-AUTO-ZONE-API
- Click on **Settings** tab (top right)
- Click on **Secrets and variables** → **Actions** (left sidebar)

### 2. Add Required Secrets

Click **"New repository secret"** for each of these:

#### Secret 1: EC2_HOST
- **Name**: `EC2_HOST`
- **Value**: `3.107.165.131`
- Click **"Add secret"**

#### Secret 2: EC2_USER
- **Name**: `EC2_USER`
- **Value**: `ec2-user`
- Click **"Add secret"**

#### Secret 3: EC2_SSH_KEY
- **Name**: `EC2_SSH_KEY`
- **Value**: Copy and paste the ENTIRE SSH key content below:

```
-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEA7UPLoz9JRLfL5wb4xChafFgtYUb0WtaCjTMSfKj/v1jkEiyw
pFzbF+Jw1SCIOdFOSLSd/C1h09evLHNkuYBXO+NYYWmu8i7LQ+L87S+p7KpBKCSd
hIVnyCCDlqiKtu5YOIrXBBKV872Apcs3+YHG43nm8THfWUT2Ilx14MSa4e7k/5EL
xiXHjbqjRtyyWkQZu+zmvZTV9vLHsFahLBgDH3/PBeS7o4SiO+2avdFYTI30rcDt
zAOVS15AKwTgSkR3E7vuhDo+iICOzBhFLS64p7hyGXQn2casPyxL70tGYpH1biHI
ta3mJE0uEKBsL2M0OS8XxZdBsoIU5J3YPPEMewIDAQABAoIBAQCycR+RSkKHfRfM
TBECLjtHc2XF2IBkZRpQqY2I1e1qcqctCBFdvDxG7VXg5JOvsDwJMFX1WAhQM9Ga
Q7sITH7PGr/Ym4wotorHJssEc6l/xdg1IbyZ819HQzTUNTQGOqF8/OaTOIswgmBj
0L/rVfBIGuFWmySYVeYrl5BMGHFH41nWcKlylH0kBA6RT/556jTf1d/xtjAOX0Lo
cQUq+EmjDPhsKjoGkWxYxrOlO5OGrUEZW/yMmpelzqKiWBtL4STpLozZFmbf18J2
tv4lM5BnUSg3fETr5xWNpkRCO9mzzD0vX1CZDhbwIIyJ59/1/mbfF5uM8w77S3yH
rB5+kuQZAoGBAP26SuXHXGN2LmNqOWHxhrYCJ6+9hQ3RxpdSCD9yUJm8TKzJeFm5
kLkHpNOYrHpQYuVvK4g3UJZ3zo4iAUuKGrpceKcXMfwd4XKMANt8hhOdAbKcd5gW
iZYiPAxSsWTWOXWrooe9YYaEAh85IRN0wrXh2ozYT1b4B5HYkk/7QQS1AoGBAO9j
wmV9KKMrM0vjkEpD6WyWDwf02PDrVQmDwmty2r7Ie2NhwjXAZ6AVhqkYAfHkSw4L
9BN6ftZf5ITr5gj6lMyaKMOjjQZmc+gAvVd6ui5jiUnhYZxzSiAzbcYqlxZLLb5K
ZZ34HOwpD3x2AbE7ppzSQYZOgGaEWIOKJgUiUzpvAoGBAK8T6zae2CtxkxTaaXoi
FRhmaEgl+DfO9r/XxQUytlc+zZG0+6y+FRT4J04y3WERMwyqJ1m5AYyyYv9Ei6w6
QbMyt7ZklQMpAzXtUXIifMnv3woGWafCdXH5cYH3VZ0FDWUa5+3OSgtt76Dn5ODu
AqVKkWn6oNScFW0YCe3Sq8y5AoGARa/euTiUCdvblO3r5RKb8vZD7ecC+C8plBl9
EVZgA0XNVYLxzD/0ao+ZocPRXR8+Ehq8tKbmIXXMyjz5vAdmJaGC2GDV/tT4TMNa
WwrpA/QJ1S39AlQ1ceZGwHdJgD3mVQzHRBMkKENTtMGNgJCC0ggK9xQHINDKC5C9
vKTfYZUCgYEAm39QbasmkYSLz73uSuCRXn0HZkOjdF8e8Sgiy//7nt/RKraizclF
xXUiyA2Q1QcWpd48mu4b683YFa2pUOQUbD9zXd6mO8Dltb5t+DIHftSbNES7/RbO
Nf67OURuM49sdKOG8EHaJ2lz2M+oUPYg/YXSm8FYtGlgNX3mU0d0bSs=
-----END RSA PRIVATE KEY-----
```

- Click **"Add secret"**

### 3. Verify Secrets
You should now have 3 secrets:
- ✅ `EC2_HOST`
- ✅ `EC2_USER` 
- ✅ `EC2_SSH_KEY`

## 🚀 Test the Deployment

### Method 1: Automatic Trigger
Make a small change and push to main:

```bash
echo "# Test deployment $(date)" >> README.md
git add .
git commit -m "test: trigger automatic deployment"
git push origin main
```

### Method 2: Manual Trigger
1. Go to GitHub repository
2. Click **"Actions"** tab
3. Select **"Deploy to EC2"** workflow
4. Click **"Run workflow"**
5. Select **"main"** branch
6. Click **"Run workflow"**

## 📊 Monitor Deployment

### View Deployment Progress
1. Go to: https://github.com/dewapathi/M-AUTO-ZONE-API/actions
2. Click on the latest workflow run
3. Watch the deployment progress in real-time

### Expected Deployment Steps
1. ✅ Checkout code
2. ✅ Setup Python
3. ✅ Install dependencies
4. ✅ Run tests
5. ✅ Create deployment package
6. ✅ Deploy to EC2
7. ✅ Extract and deploy
8. ✅ Start Docker container
9. ✅ Health check

## 🎯 Success Indicators

### GitHub Actions
- ✅ All steps show green checkmarks
- ✅ "Deploy to EC2" job completed successfully

### EC2 Deployment
- ✅ API accessible at: http://3.107.165.131:8000
- ✅ Health check passes
- ✅ Docker container running

## 🔍 Troubleshooting

### If deployment fails:
1. Check GitHub Actions logs
2. Verify SSH key is correct
3. Check EC2 instance status
4. Verify Docker is running on EC2

### Manual deployment check:
```bash
# SSH into EC2
ssh -i vehicle-parts-key.pem ec2-user@3.107.165.131

# Check container status
docker ps

# View logs
docker logs vehicle-parts-api
```

## 🎉 Success!

Once configured, every push to main branch will automatically deploy to EC2!

**API URL**: http://3.107.165.131:8000
**GitHub Actions**: https://github.com/dewapathi/M-AUTO-ZONE-API/actions
