import os
import sys
import django
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vehicle_parts_api.settings')
django.setup()

from authentication.otp_service import otp_service
from authentication.models import User

def test_send_otp(phone_number):
    """Test sending OTP"""
    print(f"\n{'='*60}")
    print(f"Testing OTP SMS to: {phone_number}")
    print(f"{'='*60}\n")
    
    if not otp_service.enabled:
        print("❌ ERROR: Twilio Verify is not enabled!")
        print("   Please set TWILIO_VERIFY_ENABLED=True in your .env file")
        return False
    
    if not otp_service.client:
        print("❌ ERROR: Twilio client not initialized!")
        print("   Please check your TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN in .env file")
        return False
    
    if not otp_service.verify_sid:
        print("❌ ERROR: TWILIO_VERIFY_SID not configured!")
        print("   Please set TWILIO_VERIFY_SID in your .env file")
        return False
    
    print("✓ Twilio Verify service is configured")
    print(f"  Account SID: {otp_service.account_sid[:10]}...")
    print(f"  Verify SID: {otp_service.verify_sid}")
    print()
    
    formatted_phone = otp_service._format_phone_number(phone_number)
    if not formatted_phone:
        print(f"❌ ERROR: Invalid phone number format: {phone_number}")
        print("   Phone number should be in format: 0779400291 or +94779400291")
        return False
    
    print(f"✓ Phone number formatted: {formatted_phone}")
    print()
    
    print("📤 Sending OTP...")
    result = otp_service.send_otp(phone_number)
    
    if result['success']:
        print("✅ SUCCESS! OTP sent successfully!")
        print(f"   Verification SID: {result.get('verification_sid', 'N/A')}")
        print(f"   Status: {result.get('status', 'N/A')}")
        print()
        print("📱 Check your phone for the OTP code!")
        return True
    else:
        print("❌ FAILED to send OTP")
        print(f"   Error: {result.get('message', 'Unknown error')}")
        return False

def test_verify_otp(phone_number, otp_code):
    """Test verifying OTP"""
    print(f"\n{'='*60}")
    print(f"Testing OTP Verification")
    print(f"Phone: {phone_number}, Code: {otp_code}")
    print(f"{'='*60}\n")
    
    result = otp_service.verify_otp(phone_number, otp_code)
    
    if result['success'] and result['verified']:
        print("✅ SUCCESS! OTP verified successfully!")
        print(f"   Status: {result.get('status', 'N/A')}")
        return True
    else:
        print("❌ FAILED to verify OTP")
        print(f"   Message: {result.get('message', 'Unknown error')}")
        print(f"   Status: {result.get('status', 'N/A')}")
        return False

if __name__ == '__main__':
    phone = "0779400291"
    
    print("\n" + "="*60)
    print("Twilio Verify OTP Test Script")
    print("="*60)
    
    if test_send_otp(phone):
        print("\n" + "-"*60)
        print("Next steps:")
        print("1. Check your phone for the OTP code")
        print("2. Run this script again with the OTP code:")
        print(f"   python test_otp.py verify <OTP_CODE>")
        print("-"*60)
    
    if len(sys.argv) > 2 and sys.argv[1] == 'verify':
        otp_code = sys.argv[2]
        test_verify_otp(phone, otp_code)

