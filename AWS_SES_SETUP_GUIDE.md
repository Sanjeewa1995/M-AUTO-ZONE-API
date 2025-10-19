# 📧 AWS SES Setup Guide for Vehicle Parts API

## 🆓 **AWS SES Free Tier (2024)**

### **Free Tier Benefits:**
- ✅ **3,000 emails/month** for first 12 months
- ✅ **62,000 emails/month** if sent from EC2
- ✅ **No cost** for receiving emails
- ✅ **Perfect for OTP emails** (low volume)

### **Pricing After Free Tier:**
- $0.10 per 1,000 emails (very affordable)
- $0.12 per 1,000 emails for attachments

## 🚀 **Step-by-Step Setup**

### **Step 1: Access AWS SES Console**

1. **Login to AWS Console**
2. **Navigate to SES:** Services → Simple Email Service
3. **Select Region:** Choose `us-east-1` (N. Virginia) for best compatibility

### **Step 2: Verify Email Address**

1. **Go to "Verified identities"**
2. **Click "Create identity"**
3. **Select "Email address"**
4. **Enter:** `noreply@vehicleparts.com` (or your domain)
5. **Click "Create identity"**
6. **Check your email** and click verification link

### **Step 3: Request Production Access**

**Important:** SES starts in "Sandbox mode" (can only send to verified emails)

1. **Go to "Account dashboard"**
2. **Click "Request production access"**
3. **Fill out the form:**
   - **Mail type:** Transactional
   - **Website URL:** Your API URL
   - **Use case description:** "Password reset OTP emails for mobile app"
   - **Expected sending volume:** 100-500 emails/month
4. **Submit request** (usually approved within 24 hours)

### **Step 4: Create SMTP Credentials**

1. **Go to "SMTP settings"**
2. **Click "Create SMTP credentials"**
3. **Enter IAM user name:** `ses-smtp-user`
4. **Download credentials** (save securely!)
5. **Note the SMTP endpoint:** `email-smtp.us-east-1.amazonaws.com`

### **Step 5: Configure Django Settings**

```bash
# Add to your .env file
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=email-smtp.us-east-1.amazonaws.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-smtp-username
EMAIL_HOST_PASSWORD=your-smtp-password
DEFAULT_FROM_EMAIL=noreply@vehicleparts.com
```

### **Step 6: Test Email Sending**

```python
# Test in Django shell
python manage.py shell -c "
from django.core.mail import send_mail
from django.conf import settings

send_mail(
    'Test Email from Vehicle Parts API',
    'This is a test email to verify SES setup.',
    settings.DEFAULT_FROM_EMAIL,
    ['malakasanjeewa1995@gmail.com'],
    fail_silently=False,
)
print('✅ Email sent successfully!')
"
```

## 🔧 **Alternative: Gmail SMTP (Free & Easy)**

If you want to start immediately without AWS setup:

```bash
# Gmail SMTP Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@vehicleparts.com
```

**Gmail Setup:**
1. Enable 2-Factor Authentication
2. Generate App Password: Google Account → Security → App passwords
3. Use app password (not regular password)

## 📊 **Cost Comparison**

| Service | Free Tier | Cost After Free |
|---------|-----------|-----------------|
| **AWS SES** | 3,000 emails/month | $0.10/1,000 emails |
| **Gmail SMTP** | Unlimited* | Free |
| **SendGrid** | 100 emails/day | $14.95/month |

*Gmail has daily limits (~500 emails/day)

## 🚀 **Quick Start (Recommended)**

For immediate testing, use Gmail SMTP:

1. **Set up Gmail app password**
2. **Update your .env file** with Gmail settings
3. **Test OTP email** immediately
4. **Switch to AWS SES** later for production

## 📱 **Mobile App Integration**

Your OTP emails will look like this:

```
Subject: Password Reset OTP - Vehicle Parts API

Hello Malaka,

You have requested to reset your password for the Vehicle Parts API.

Your OTP is: 369868

This OTP will expire in 10 minutes.

If you did not request this password reset, please ignore this email.

Best regards,
Vehicle Parts API Team
```

## 🔒 **Security Best Practices**

1. **Use environment variables** for credentials
2. **Verify sending domain** for better deliverability
3. **Monitor bounce rates** in AWS SES console
4. **Set up CloudWatch alarms** for failed emails
5. **Use dedicated email** for API (not personal Gmail)

## 📈 **Monitoring & Analytics**

### **AWS SES Console:**
- **Sending statistics**
- **Bounce and complaint rates**
- **Reputation monitoring**
- **Delivery logs**

### **Django Logging:**
```python
# Add to settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'email.log',
        },
    },
    'loggers': {
        'django.core.mail': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## 🎯 **Recommendation**

**For your use case (OTP emails):**
1. **Start with Gmail SMTP** (immediate setup)
2. **Switch to AWS SES** for production (better deliverability)
3. **Monitor usage** to stay within free tier

**Your OTP system will work perfectly with either option! 🚀**
