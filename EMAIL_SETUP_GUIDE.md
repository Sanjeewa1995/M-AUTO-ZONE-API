# 📧 Email Configuration Guide for Vehicle Parts API

## 🔧 **Production Email Setup**

### **Option 1: Gmail SMTP (Recommended for Development)**

```bash
# Add to your .env file
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@vehicleparts.com
```

**Gmail Setup Steps:**
1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account Settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. Use the app password (not your regular password)

### **Option 2: AWS SES (Recommended for Production)**

```bash
# Add to your .env file
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=email-smtp.us-east-1.amazonaws.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-ses-smtp-username
EMAIL_HOST_PASSWORD=your-ses-smtp-password
DEFAULT_FROM_EMAIL=noreply@vehicleparts.com
```

**AWS SES Setup Steps:**
1. Create AWS SES SMTP credentials
2. Verify your domain or email address
3. Request production access if needed

### **Option 3: SendGrid**

```bash
# Add to your .env file
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
DEFAULT_FROM_EMAIL=noreply@vehicleparts.com
```

## 🧪 **Testing Email Configuration**

### **Test Email Sending:**

```python
# Run this in Django shell
python manage.py shell -c "
from django.core.mail import send_mail
from django.conf import settings

# Test email
send_mail(
    'Test Email',
    'This is a test email from Vehicle Parts API',
    settings.DEFAULT_FROM_EMAIL,
    ['malakasanjeewa1995@gmail.com'],
    fail_silently=False,
)
print('Email sent successfully!')
"
```

### **Test OTP Email:**

```python
# Test the full OTP flow
python manage.py shell -c "
from authentication.models import User
from authentication.views import password_reset_request_view
from django.test import RequestFactory
import json

# Get user and request OTP
user = User.objects.get(email='malakasanjeewa1995@gmail.com')
otp = user.generate_reset_otp()
print(f'OTP generated: {otp}')

# This will send actual email if configured
factory = RequestFactory()
request = factory.post('/api/v1/auth/password-reset/', 
    json.dumps({'email': 'malakasanjeewa1995@gmail.com'}),
    content_type='application/json'
)

# Test the view (will send email)
response = password_reset_request_view(request)
print(f'Response: {response.data}')
"
```

## 🔒 **Security Best Practices**

1. **Use Environment Variables:** Never hardcode email credentials
2. **Use App Passwords:** For Gmail, use app passwords, not regular passwords
3. **Verify Domains:** For production, verify your sending domain
4. **Rate Limiting:** Implement rate limiting for OTP requests
5. **OTP Expiration:** OTPs expire in 10 minutes
6. **Account Lockout:** 3 failed attempts = 15-minute lockout

## 📱 **Mobile App Integration**

### **OTP Flow for Mobile Apps:**

1. **Request OTP:**
   ```json
   POST /api/v1/auth/password-reset/
   {
     "email": "user@example.com"
   }
   ```

2. **Verify OTP:**
   ```json
   POST /api/v1/auth/verify-otp/
   {
     "email": "user@example.com",
     "otp": "123456"
   }
   ```

3. **Reset Password:**
   ```json
   POST /api/v1/auth/password-reset/confirm/
   {
     "email": "user@example.com",
     "otp": "123456",
     "new_password": "newpassword123",
     "new_password_confirm": "newpassword123"
   }
   ```

## 🚀 **Deployment Checklist**

- [ ] Configure email backend in production
- [ ] Set up SMTP credentials
- [ ] Test email sending
- [ ] Verify OTP emails are received
- [ ] Test complete password reset flow
- [ ] Monitor email delivery rates
- [ ] Set up email logging

---

**Your OTP-based password reset is ready for production! 🎉**
