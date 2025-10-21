#!/usr/bin/env python3
"""
Simple email test script for Vehicle Parts API
"""
import os
import django
from decouple import config

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vehicle_parts_api.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("🔧 Testing Email Configuration")
print("=" * 50)
print(f"📧 Email Backend: {settings.EMAIL_BACKEND}")
print(f"📧 Email Host: {settings.EMAIL_HOST}")
print(f"📧 Email Port: {settings.EMAIL_PORT}")
print(f"📧 Email TLS: {settings.EMAIL_USE_TLS}")
print(f"📧 From Email: {settings.DEFAULT_FROM_EMAIL}")
print("=" * 50)

# Test email sending
print("🧪 Sending test email...")
try:
    send_mail(
        subject='Test Email - Vehicle Parts API',
        message='This is a test email to verify email configuration.\n\nIf you receive this, email is working correctly!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['malakasanjeewa1995@gmail.com'],
        fail_silently=False,
    )
    print("✅ Email sent successfully!")
    print("📬 Check your email inbox for the test message")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
    print("\n🔧 Troubleshooting:")
    print("1. Check your Gmail app password")
    print("2. Make sure 2FA is enabled")
    print("3. Verify EMAIL_HOST_PASSWORD in .env.local")
    print("4. Check Gmail security settings")

print("\n🎉 Email test completed!")
