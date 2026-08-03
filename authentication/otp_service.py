"""
OTP service using SMSlenz for sending SMS and database for storage
"""
import logging
import requests
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)


class OTPVerificationService:
    """
    Service for OTP generation, sending via SMSlenz, and verification using database
    """
    
    def __init__(self):
        self.user_id = getattr(settings, 'SMSLENZ_USER_ID', '')
        self.api_key = getattr(settings, 'SMSLENZ_API_KEY', '')
        self.sender_id = getattr(settings, 'SMSLENZ_SENDER_ID', '')
        self.enabled = getattr(settings, 'SMSLENZ_ENABLED', False)
        self.api_url = 'https://smslenz.lk/api/send-sms'
        self.otp_expiry_minutes = 10  # OTP expires in 10 minutes
        
    def send_otp(self, user):
        """
        Generate OTP, store it in user's reset_otp field, and send via SMSlenz
        
        Args:
            user: User model instance
            
        Returns:
            dict: Result dictionary with 'success' (bool) and 'message' (str)
        """
        if not self.enabled:
            return {
                'success': False,
                'message': 'SMSlenz OTP service is not enabled'
            }
        
        if not self.user_id or not self.api_key or not self.sender_id:
            return {
                'success': False,
                'message': 'SMSlenz configuration incomplete. Please check SMSLENZ_USER_ID, SMSLENZ_API_KEY, and SMSLENZ_SENDER_ID in your .env file.'
            }
        
        if not user or not user.phone:
            return {
                'success': False,
                'message': 'User and phone number are required'
            }
        
        # Format phone number
        phone_number = self._format_phone_number(user.phone)
        if not phone_number:
            return {
                'success': False,
                'message': 'Invalid phone number format. Please use E.164 format (e.g., +94771234567)'
            }
        
        # Generate and store OTP using User model's method
        otp_code = user.generate_reset_otp()
        
        # Create SMS message
        message = f"Your password reset OTP for Vehicle Parts API is: {otp_code}. This OTP will expire in {self.otp_expiry_minutes} minutes. If you did not request this, please ignore this message."
        
        # Send SMS via SMSlenz API
        try:
            payload = {
                'user_id': self.user_id,
                'api_key': self.api_key,
                'sender_id': self.sender_id,
                'contact': phone_number,
                'message': message
            }
            
            response = requests.post(self.api_url, data=payload, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            
            # Check if SMS was sent successfully
            # SMSlenz API returns: {"message": "SMS sent successfully", "data": {"status": "success", "campaign_id": ...}}
            data = result.get('data', {})
            status_in_data = data.get('status', '')
            campaign_id = data.get('campaign_id')
            
            if response.status_code == 200 and (status_in_data == 'success' or campaign_id is not None):
                logger.info(f"OTP sent successfully to {phone_number} via SMSlenz. OTP: {otp_code}, Campaign ID: {campaign_id}")
                return {
                    'success': True,
                    'message': 'OTP sent successfully'
                }
            else:
                error_msg = result.get('message', 'Failed to send SMS')
                logger.error(f"Failed to send OTP via SMSlenz: {error_msg}")
                # Clear OTP since SMS failed
                user.clear_reset_otp()
                return {
                    'success': False,
                    'message': f'Failed to send OTP: {error_msg}'
                }
                
        except requests.exceptions.RequestException as e:
            error_msg = f'Failed to send OTP via SMSlenz: {str(e)}'
            logger.error(error_msg)
            # Clear OTP since SMS failed
            user.clear_reset_otp()
            return {
                'success': False,
                'message': 'Failed to send OTP. Please try again later.'
            }
        except Exception as e:
            error_msg = f'Unexpected error sending OTP: {str(e)}'
            logger.error(error_msg)
            # Clear OTP since SMS failed
            user.clear_reset_otp()
            return {
                'success': False,
                'message': 'Failed to send OTP. Please try again later.'
            }
    
    def verify_otp(self, user, code):
        """
        Verify OTP code against user's reset_otp field in database
        
        Args:
            user: User model instance
            code (str): OTP code entered by user
            
        Returns:
            dict: Result dictionary with 'success' (bool), 'verified' (bool), 'message' (str)
        """
        if not self.enabled:
            return {
                'success': False,
                'verified': False,
                'message': 'OTP verification is not enabled'
            }
        
        if not user or not code:
            return {
                'success': False,
                'verified': False,
                'message': 'User and OTP code are required'
            }
        
        # Verify OTP using User model's method
        is_valid, message = user.is_otp_valid(code)
        
        if is_valid:
            logger.info(f"OTP verified successfully for user {user.phone}")
            return {
                'success': True,
                'verified': True,
                'message': 'OTP verified successfully',
                'status': 'approved'
            }
        else:
            logger.warning(f"OTP verification failed for {user.phone}: {message}")
            return {
                'success': False,
                'verified': False,
                'message': message,
                'status': 'invalid' if 'Invalid' in message else 'expired' if 'expired' in message else 'locked' if 'locked' in message else 'error'
            }
    
    def _format_phone_number(self, phone_number):
        """
        Format phone number to E.164 format for SMSlenz (must include +94 for Sri Lanka)
        
        Args:
            phone_number (str): Phone number in various formats
            
        Returns:
            str: Formatted phone number in E.164 format, or None if invalid
        """
        if not phone_number:
            return None
        
        # Remove spaces, dashes, parentheses, and other non-digit/+ characters
        cleaned = ''.join(char for char in phone_number if char.isdigit() or char == '+')
        
        # If already starts with +, validate it
        if cleaned.startswith('+'):
            digits_only = cleaned[1:]
            # Must be 10-15 digits
            if digits_only.isdigit() and 10 <= len(digits_only) <= 15:
                return cleaned
            else:
                return None
        
        # Sri Lankan numbers: 0XXXXXXXXX or 07XXXXXXXX (remove leading 0, add +94)
        if cleaned.startswith('0'):
            if len(cleaned) >= 9:
                return '+94' + cleaned[1:]
        
        # If already 9-10 digits without +, assume Sri Lankan and add +94
        if 9 <= len(cleaned) <= 10 and cleaned.isdigit():
            # Check if it looks like a Sri Lankan mobile (starts with 7)
            if cleaned[0] == '7' or (cleaned.startswith('0') and cleaned[1] == '7'):
                if cleaned.startswith('0'):
                    return '+94' + cleaned[1:]
                else:
                    return '+94' + cleaned
        
        # Basic validation
        if len(cleaned) < 9 or len(cleaned) > 15:
            return None
        
        return None


# Singleton instance
otp_service = OTPVerificationService()
