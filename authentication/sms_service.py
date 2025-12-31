"""
SMS messaging service using Twilio
"""
import logging
from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioException

logger = logging.getLogger(__name__)


class SMSService:
    """
    Service for sending SMS messages via Twilio
    """
    
    def __init__(self):
        self.account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', '')
        self.auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', '')
        self.sms_from = getattr(settings, 'TWILIO_SMS_FROM', '')
        self.enabled = getattr(settings, 'TWILIO_SMS_ENABLED', False)
        
        if self.enabled and self.account_sid and self.auth_token:
            try:
                self.client = Client(self.account_sid, self.auth_token)
            except Exception as e:
                logger.error(f"Failed to initialize Twilio SMS client: {str(e)}")
                self.client = None
        else:
            self.client = None
    
    def send_sms(self, to_number, message_body):
        """
        Send SMS message to a phone number
        
        Args:
            to_number (str): Recipient phone number in E.164 format (e.g., +94771234567)
            message_body (str): Message content to send
            
        Returns:
            dict: Result dictionary with 'success' (bool) and 'message' (str)
        """
        if not self.enabled:
            return {
                'success': False,
                'message': 'SMS messaging is not enabled'
            }
        
        if not self.client:
            return {
                'success': False,
                'message': 'Twilio client not initialized. Please check your configuration.'
            }
        
        if not to_number:
            return {
                'success': False,
                'message': 'Recipient phone number is required'
            }
        
        if not self.sms_from:
            return {
                'success': False,
                'message': 'TWILIO_SMS_FROM is not configured. Please set it in your .env file.'
            }
        
        # Ensure phone number is in correct format
        to_number = self._format_phone_number(to_number)
        if not to_number:
            return {
                'success': False,
                'message': f'Invalid phone number format: "{to_number}". Please use E.164 format (e.g., +94771234567)'
            }
        
        try:
            message = self.client.messages.create(
                body=message_body,
                from_=self.sms_from,
                to=to_number
            )
            
            logger.info(f"SMS sent successfully. SID: {message.sid}, To: {to_number}")
            return {
                'success': True,
                'message': 'SMS sent successfully',
                'message_sid': message.sid
            }
            
        except TwilioException as e:
            error_str = str(e)
            error_msg = f'Failed to send SMS: {error_str}'
            logger.error(error_msg)
            
            # Provide helpful guidance for common errors
            if '21212' in error_str or "not a valid phone number" in error_str.lower():
                return {
                    'success': False,
                    'message': f'Invalid phone number format. Please use E.164 format (e.g., +94771234567). Error: {error_str}'
                }
            elif '21211' in error_str or "To number" in error_str:
                return {
                    'success': False,
                    'message': f'Invalid recipient phone number: {to_number}'
                }
            
            return {
                'success': False,
                'message': error_msg
            }
        except Exception as e:
            error_msg = f'Unexpected error sending SMS: {str(e)}'
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg
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
        
        # Remove spaces, dashes, parentheses, and other non-digit/+ characters
        cleaned = ''.join(char for char in phone_number if char.isdigit() or char == '+')
        
        # If already starts with +, validate it
        if cleaned.startswith('+'):
            # Remove the + to check digits
            digits_only = cleaned[1:]
            # Must be 10-15 digits
            if digits_only.isdigit() and 10 <= len(digits_only) <= 15:
                return cleaned
            else:
                return None
        
        # If doesn't start with +, try to detect country code
        # Common patterns:
        # - Sri Lankan: 0XXXXXXXXX or 07XXXXXXXX (remove leading 0, add +94)
        # - US/Canada: 10 digits, add +1
        # - UK: starts with 0, add +44
        
        # Check if it starts with 0 (common in many countries)
        if cleaned.startswith('0'):
            # Sri Lankan mobile numbers: 07XXXXXXXX (9 digits after 0)
            if len(cleaned) >= 9:
                # Remove leading 0 and add Sri Lanka country code +94
                return '+94' + cleaned[1:]
        
        # US/Canada: 10 digits, add +1
        if len(cleaned) == 10 and cleaned.isdigit():
            return '+1' + cleaned
        
        # UK: If starts with 0 and is 11 digits, add +44
        if cleaned.startswith('0') and len(cleaned) == 11:
            return '+44' + cleaned[1:]
        
        # If already 10-15 digits without +, assume it needs country code
        # Try Sri Lanka first (+94) as it's common format
        if 9 <= len(cleaned) <= 10 and cleaned.isdigit():
            # Check if it looks like a Sri Lankan mobile (starts with 7)
            if cleaned[0] == '7' or (cleaned.startswith('0') and cleaned[1] == '7'):
                if cleaned.startswith('0'):
                    return '+94' + cleaned[1:]
                else:
                    return '+94' + cleaned
        
        # Default: if 10 digits, assume US (+1)
        if len(cleaned) == 10 and cleaned.isdigit():
            return '+1' + cleaned
        
        # Basic validation - should be 10-15 digits after country code
        if len(cleaned) < 9 or len(cleaned) > 15:
            return None
        
        # If we can't format it properly, return None
        return None


# Singleton instance
sms_service = SMSService()

