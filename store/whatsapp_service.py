"""
WhatsApp messaging service using Twilio
"""
import logging
from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioException

logger = logging.getLogger(__name__)


class WhatsAppService:
    """
    Service for sending WhatsApp messages via Twilio
    """
    
    def __init__(self):
        self.account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', '')
        self.auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', '')
        whatsapp_from_raw = getattr(settings, 'TWILIO_WHATSAPP_FROM', '')
        # Remove 'whatsapp:' prefix if present (we add it in send_message)
        if whatsapp_from_raw.startswith('whatsapp:'):
            self.whatsapp_from = whatsapp_from_raw.replace('whatsapp:', '')
        else:
            self.whatsapp_from = whatsapp_from_raw
        self.enabled = getattr(settings, 'TWILIO_WHATSAPP_ENABLED', False)
        
        if self.enabled and self.account_sid and self.auth_token:
            try:
                self.client = Client(self.account_sid, self.auth_token)
            except Exception as e:
                logger.error(f"Failed to initialize Twilio client: {str(e)}")
                self.client = None
        else:
            self.client = None
    
    def send_message(self, to_number, message_body):
        """
        Send WhatsApp message to a phone number
        
        Args:
            to_number (str): Recipient phone number in E.164 format (e.g., +1234567890)
            message_body (str): Message content to send
            
        Returns:
            dict: Result dictionary with 'success' (bool) and 'message' (str)
        """
        if not self.enabled:
            return {
                'success': False,
                'message': 'WhatsApp messaging is not enabled'
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
        
        # Ensure phone number is in correct format
        original_number = to_number  # Keep for error messages
        to_number = self._format_phone_number(to_number)
        if not to_number:
            return {
                'success': False,
                'message': f'Invalid phone number format: "{original_number}". Please use E.164 format (e.g., +94710742371 for Sri Lanka, +1234567890 for US)'
            }
        
        try:
            message = self.client.messages.create(
                body=message_body,
                from_=f'whatsapp:{self.whatsapp_from}',
                to=f'whatsapp:{to_number}'
            )
            
            logger.info(f"WhatsApp message sent successfully. SID: {message.sid}")
            return {
                'success': True,
                'message': 'WhatsApp message sent successfully',
                'message_sid': message.sid
            }
            
        except TwilioException as e:
            error_str = str(e)
            error_msg = f'Failed to send WhatsApp message: {error_str}'
            logger.error(error_msg)
            
            # Provide helpful guidance for common errors
            if '21212' in error_str or "not a valid phone number" in error_str.lower() or "not a valid" in error_str.lower():
                return {
                    'success': False,
                    'message': f'Invalid WhatsApp "From" number: {self.whatsapp_from}. '
                               f'Please verify your TWILIO_WHATSAPP_FROM in your .env file. '
                               f'For testing, you need to join Twilio WhatsApp Sandbox first. '
                               f'For production, use your approved WhatsApp Business number.'
                }
            elif '21211' in error_str or "To number" in error_str:
                return {
                    'success': False,
                    'message': f'Invalid recipient phone number. Please check the shop phone number format.'
                }
            
            return {
                'success': False,
                'message': error_msg
            }
        except Exception as e:
            error_msg = f'Unexpected error sending WhatsApp message: {str(e)}'
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
            # Also handles landlines: 0XX-XXXXXXX
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
whatsapp_service = WhatsAppService()

