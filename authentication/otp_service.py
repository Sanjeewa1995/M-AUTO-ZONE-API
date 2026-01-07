import logging
from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioException

logger = logging.getLogger(__name__)


class OTPVerificationService:
    """
    Service for OTP verification via Twilio Verify API
    """
    
    def __init__(self):
        self.account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', '')
        self.auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', '')
        self.verify_sid = getattr(settings, 'TWILIO_VERIFY_SID', '')
        self.enabled = getattr(settings, 'TWILIO_VERIFY_ENABLED', False)
        
        if self.enabled and self.account_sid and self.auth_token and self.verify_sid:
            try:
                self.client = Client(self.account_sid, self.auth_token)
            except Exception as e:
                logger.error(f"Failed to initialize Twilio Verify client: {str(e)}")
                self.client = None
        else:
            self.client = None
    
    def send_otp(self, phone_number):
        """
        Send OTP to a phone number using Twilio Verify
        
        Args:
            phone_number (str): Recipient phone number in E.164 format (e.g., +94771234567)
            
        Returns:
            dict: Result dictionary with 'success' (bool) and 'message' (str)
        """
        if not self.enabled:
            return {
                'success': False,
                'message': 'OTP verification is not enabled'
            }
        
        if not self.client:
            return {
                'success': False,
                'message': 'Twilio Verify client not initialized. Please check your configuration.'
            }
        
        if not phone_number:
            return {
                'success': False,
                'message': 'Phone number is required'
            }
        
        if not self.verify_sid:
            return {
                'success': False,
                'message': 'TWILIO_VERIFY_SID is not configured. Please set it in your .env file.'
            }
        
        # Ensure phone number is in correct format
        phone_number = self._format_phone_number(phone_number)
        if not phone_number:
            return {
                'success': False,
                'message': f'Invalid phone number format. Please use E.164 format (e.g., +94771234567)'
            }
        
        try:
            verification = self.client.verify.v2.services(self.verify_sid) \
                .verifications.create(to=phone_number, channel='sms')
            
            logger.info(f"OTP verification sent successfully. SID: {verification.sid}, To: {phone_number}, Status: {verification.status}")
            return {
                'success': True,
                'message': 'OTP sent successfully',
                'verification_sid': verification.sid,
                'status': verification.status
            }
            
        except TwilioException as e:
            error_str = str(e)
            error_msg = f'Failed to send OTP: {error_str}'
            logger.error(error_msg)
            
            if '21212' in error_str or "not a valid phone number" in error_str.lower():
                return {
                    'success': False,
                    'message': f'Invalid phone number format. Please use E.164 format (e.g., +94771234567). Error: {error_str}'
                }
            elif '60200' in error_str or "Invalid parameter" in error_str:
                return {
                    'success': False,
                    'message': f'Invalid verification service configuration. Please check TWILIO_VERIFY_SID.'
                }
            
            return {
                'success': False,
                'message': error_msg
            }
        except Exception as e:
            error_msg = f'Unexpected error sending OTP: {str(e)}'
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg
            }
    
    def verify_otp(self, phone_number, code):
        """
        Verify OTP code using Twilio Verify
        
        Args:
            phone_number (str): Phone number in E.164 format (e.g., +94771234567)
            code (str): OTP code entered by user
            
        Returns:
            dict: Result dictionary with 'success' (bool), 'verified' (bool), 'message' (str), and 'status' (str)
        """
        if not self.enabled:
            return {
                'success': False,
                'verified': False,
                'message': 'OTP verification is not enabled'
            }
        
        if not self.client:
            return {
                'success': False,
                'verified': False,
                'message': 'Twilio Verify client not initialized. Please check your configuration.'
            }
        
        if not phone_number or not code:
            return {
                'success': False,
                'verified': False,
                'message': 'Phone number and OTP code are required'
            }
        
        if not self.verify_sid:
            return {
                'success': False,
                'verified': False,
                'message': 'TWILIO_VERIFY_SID is not configured. Please set it in your .env file.'
            }
        
        phone_number = self._format_phone_number(phone_number)
        if not phone_number:
            return {
                'success': False,
                'verified': False,
                'message': f'Invalid phone number format. Please use E.164 format (e.g., +94771234567)'
            }
        
        try:
            verification_check = self.client.verify.v2.services(self.verify_sid) \
                .verification_checks.create(to=phone_number, code=code)
            
            is_verified = verification_check.status == 'approved'
            
            logger.info(f"OTP verification check. SID: {verification_check.sid}, To: {phone_number}, Status: {verification_check.status}, Verified: {is_verified}")
            
            return {
                'success': True,
                'verified': is_verified,
                'status': verification_check.status,
                'message': 'OTP verified successfully' if is_verified else 'Invalid or expired OTP code',
                'verification_check_sid': verification_check.sid
            }
            
        except TwilioException as e:
            error_str = str(e)
            error_msg = f'Failed to verify OTP: {error_str}'
            logger.error(error_msg)
            
            if '20404' in error_str or "not found" in error_str.lower():
                return {
                    'success': False,
                    'verified': False,
                    'message': 'OTP verification not found. Please request a new OTP.',
                    'status': 'not_found'
                }
            elif '60203' in error_str or "Max check attempts" in error_str:
                return {
                    'success': False,
                    'verified': False,
                    'message': 'Maximum verification attempts exceeded. Please request a new OTP.',
                    'status': 'max_attempts_exceeded'
                }
            
            return {
                'success': False,
                'verified': False,
                'message': error_msg,
                'status': 'error'
            }
        except Exception as e:
            error_msg = f'Unexpected error verifying OTP: {str(e)}'
            logger.error(error_msg)
            return {
                'success': False,
                'verified': False,
                'message': error_msg,
                'status': 'error'
            }
    
    def _format_phone_number(self, phone_number):
        """
        Format phone number to E.164 format
        
        Args:
            phone_number (str): Phone number in various formats
            
        Returns:
            str: Formatted phone number in E.164 format, or None if invalid
        """
        if not phone_number:
            return None
        
        cleaned = ''.join(char for char in phone_number if char.isdigit() or char == '+')
        
        if cleaned.startswith('+'):
            digits_only = cleaned[1:]
            if digits_only.isdigit() and 10 <= len(digits_only) <= 15:
                return cleaned
            else:
                return None
            
        if cleaned.startswith('0'):
            if len(cleaned) >= 9:
                return '+94' + cleaned[1:]
        
        if len(cleaned) == 10 and cleaned.isdigit():
            return '+1' + cleaned
        
        if cleaned.startswith('0') and len(cleaned) == 11:
            return '+44' + cleaned[1:]
        
        if 9 <= len(cleaned) <= 10 and cleaned.isdigit():
            if cleaned[0] == '7' or (cleaned.startswith('0') and cleaned[1] == '7'):
                if cleaned.startswith('0'):
                    return '+94' + cleaned[1:]
                else:
                    return '+94' + cleaned
        
        if len(cleaned) == 10 and cleaned.isdigit():
            return '+1' + cleaned
        
        if len(cleaned) < 9 or len(cleaned) > 15:
            return None
        
        return None


otp_service = OTPVerificationService()

