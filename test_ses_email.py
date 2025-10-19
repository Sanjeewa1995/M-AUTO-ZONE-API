#!/usr/bin/env python
"""
Test script for AWS SES email configuration
Run this after setting up your SES credentials
"""

import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vehicle_parts_api.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_ses_email():
    """Test AWS SES email sending"""
    try:
        print("🧪 Testing AWS SES email configuration...")
        print(f"📧 Email Backend: {settings.EMAIL_BACKEND}")
        print(f"📧 Email Host: {settings.EMAIL_HOST}")
        print(f"📧 From Email: {settings.DEFAULT_FROM_EMAIL}")
        
        # Send test email
        send_mail(
            subject='Test Email from Vehicle Parts API - AWS SES',
            message='This is a test email to verify AWS SES configuration.\n\nIf you receive this, SES is working correctly!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['malakasanjeewa1995@gmail.com'],
            fail_silently=False,
        )
        
        print("✅ Email sent successfully!")
        print("📬 Check your email inbox for the test message")
        
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your SMTP credentials")
        print("2. Verify your email address in SES")
        print("3. Ensure production access is approved")
        print("4. Check AWS SES console for any restrictions")

def test_otp_email():
    """Test OTP email format"""
    try:
        print("\n🧪 Testing OTP email format...")
        
        otp = "123456"  # Test OTP
        user_name = "Malaka"
        
        html_message = f"""
        <html>
        <body>
            <h2>Password Reset OTP</h2>
            <p>Hello {user_name},</p>
            <p>You have requested to reset your password for the Vehicle Parts API.</p>
            <p>Your OTP is: <strong style="font-size: 24px; color: #007bff;">{otp}</strong></p>
            <p>This OTP will expire in 10 minutes.</p>
            <p>If you did not request this password reset, please ignore this email.</p>
            <br>
            <p>Best regards,<br>Vehicle Parts API Team</p>
        </body>
        </html>
        """
        
        plain_message = f"""
        Password Reset OTP
        
        Hello {user_name},
        
        You have requested to reset your password for the Vehicle Parts API.
        
        Your OTP is: {otp}
        
        This OTP will expire in 10 minutes.
        
        If you did not request this password reset, please ignore this email.
        
        Best regards,
        Vehicle Parts API Team
        """
        
        send_mail(
            subject='Password Reset OTP - Vehicle Parts API',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['malakasanjeewa1995@gmail.com'],
            html_message=html_message,
            fail_silently=False,
        )
        
        print("✅ OTP email sent successfully!")
        print("📬 Check your email for the OTP message")
        
    except Exception as e:
        print(f"❌ Error sending OTP email: {e}")

if __name__ == "__main__":
    print("🚀 AWS SES Email Testing")
    print("=" * 50)
    
    # Test basic email
    test_ses_email()
    
    # Test OTP email format
    test_otp_email()
    
    print("\n🎉 Testing complete!")
    print("If emails were sent successfully, your AWS SES setup is working!")
