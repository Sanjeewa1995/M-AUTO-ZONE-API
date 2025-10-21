#!/usr/bin/env python3
"""
AWS SES Credentials Test Script
==============================

This script tests the AWS SES SMTP credentials to verify they work.
Run this after checking your AWS SES console configuration.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_ses_credentials():
    """Test AWS SES SMTP credentials"""
    
    # SES Configuration
    smtp_host = "email-smtp.ap-southeast-2.amazonaws.com"
    smtp_port = 587
    smtp_username = "AKIASCRDKW6LGEB73W4E"
    smtp_password = "BLanh3xQY9lE7eTL6rElPtE/nxN+R2TRyUQ66cxbdN5m"
    
    # Email details
    from_email = "malakasanjeewa1995@gmail.com"
    to_email = "malakasanjeewa1995@gmail.com"  # Make sure this is verified in SES
    
    print("🧪 Testing AWS SES Credentials")
    print("==============================")
    print(f"SMTP Host: {smtp_host}")
    print(f"SMTP Port: {smtp_port}")
    print(f"Username: {smtp_username}")
    print(f"From: {from_email}")
    print(f"To: {to_email}")
    print("")
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = "AWS SES Test Email"
        
        body = """
        This is a test email to verify AWS SES SMTP credentials.
        
        If you receive this email, your SES configuration is working correctly!
        
        Best regards,
        Vehicle Parts API Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to SMTP server
        print("🔌 Connecting to AWS SES SMTP server...")
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()  # Enable TLS encryption
        
        # Login with credentials
        print("🔑 Authenticating with AWS SES...")
        server.login(smtp_username, smtp_password)
        
        # Send email
        print("📧 Sending test email...")
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        
        print("✅ Email sent successfully!")
        print("📬 Check your email inbox for the test message")
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("🔧 Possible solutions:")
        print("   - Check if SMTP credentials are correct")
        print("   - Verify credentials in AWS SES console")
        print("   - Generate new SMTP credentials if needed")
        
    except smtplib.SMTPRecipientsRefused as e:
        print(f"❌ Recipient refused: {e}")
        print("🔧 Possible solutions:")
        print("   - Verify recipient email in AWS SES")
        print("   - Check if SES is in sandbox mode")
        print("   - Make sure recipient email is verified")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("🔧 Check your AWS SES configuration")

if __name__ == "__main__":
    test_ses_credentials()
