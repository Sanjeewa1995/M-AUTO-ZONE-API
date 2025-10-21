#!/usr/bin/env python3
"""
Update AWS SES Credentials Script
================================

This script helps you update the AWS SES credentials in your configuration files.
Run this after getting new SMTP credentials from AWS SES console.
"""

import os
import re

def update_ses_credentials():
    """Update SES credentials in configuration files"""
    
    print("🔧 AWS SES Credentials Update")
    print("============================")
    print("")
    print("📋 Please provide the new SMTP credentials from AWS SES console:")
    print("")
    
    # Get new credentials from user
    new_username = input("Enter new SMTP Username: ").strip()
    new_password = input("Enter new SMTP Password: ").strip()
    
    if not new_username or not new_password:
        print("❌ Username and password are required!")
        return
    
    print("")
    print("🔄 Updating configuration files...")
    
    # Files to update
    files_to_update = [
        '.github/workflows/deploy.yml',
        'env.production.ses',
        'test_ses_credentials.py'
    ]
    
    for file_path in files_to_update:
        if os.path.exists(file_path):
            print(f"📝 Updating {file_path}...")
            update_file_credentials(file_path, new_username, new_password)
        else:
            print(f"⚠️  File not found: {file_path}")
    
    print("")
    print("✅ Credentials updated successfully!")
    print("")
    print("🧪 Test the new credentials:")
    print("python test_ses_credentials.py")
    print("")
    print("🚀 Deploy the updated configuration:")
    print("git add . && git commit -m 'update: New AWS SES credentials' && git push origin main")

def update_file_credentials(file_path, new_username, new_password):
    """Update credentials in a specific file"""
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Update EMAIL_HOST_USER
        content = re.sub(
            r'EMAIL_HOST_USER=AKIASCRDKW6LMO3EDX57',
            f'EMAIL_HOST_USER={new_username}',
            content
        )
        
        # Update EMAIL_HOST_PASSWORD
        content = re.sub(
            r'EMAIL_HOST_PASSWORD=4KKUNby5FNClDBompEml9d7pHLgZZk2V4N/WUSH9',
            f'EMAIL_HOST_PASSWORD={new_password}',
            content
        )
        
        # Update smtp_username in test script
        content = re.sub(
            r'smtp_username = "AKIASCRDKW6LMO3EDX57"',
            f'smtp_username = "{new_username}"',
            content
        )
        
        # Update smtp_password in test script
        content = re.sub(
            r'smtp_password = "4KKUNby5FNClDBompEml9d7pHLgZZk2V4N/WUSH9"',
            f'smtp_password = "{new_password}"',
            content
        )
        
        with open(file_path, 'w') as f:
            f.write(content)
        
        print(f"✅ Updated {file_path}")
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")

if __name__ == "__main__":
    update_ses_credentials()
