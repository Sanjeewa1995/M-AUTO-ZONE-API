# 📧 Gmail SMTP Setup Guide

## Step 1: Enable 2-Factor Authentication
1. Go to your Google Account settings
2. Navigate to Security → 2-Step Verification
3. Enable 2-Factor Authentication

## Step 2: Generate App Password
1. Go to Google Account → Security → 2-Step Verification
2. Scroll down to "App passwords"
3. Select "Mail" and "Other (custom name)"
4. Enter "Vehicle Parts API"
5. Copy the generated 16-character password

## Step 3: Update Environment Variables
Replace `your-gmail-app-password-here` with your actual app password:

```bash
# Update .env.local file
EMAIL_HOST_PASSWORD=your-actual-16-character-app-password
```

## Step 4: Test Email Sending
```bash
# Test the configuration
python test_email_local.py
```

## Alternative: Use Console Backend for Development
If you want to see emails in server logs (for development):

```bash
# Update .env.local
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

## Troubleshooting
- Make sure 2FA is enabled
- Use App Password, not your regular password
- Check Gmail security settings
- Verify the 16-character app password is correct
