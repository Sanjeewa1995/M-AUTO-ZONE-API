"""
Custom validators for authentication app
"""
import re
from django.core.exceptions import ValidationError


def validate_sri_lankan_phone_number(value):
    """
    Validate and normalize Sri Lankan phone numbers
    
    Accepts formats:
    - +94771234567 (E.164 format)
    - 94771234567 (without +)
    - 0771234567 (local format with leading 0)
    - 071234567 (local format without leading 0 for some numbers)
    
    Returns normalized format: +94771234567
    """
    if not value:
        raise ValidationError("Phone number is required")
    
    # Remove all spaces, dashes, and parentheses
    phone = re.sub(r'[\s\-\(\)]', '', str(value).strip())
    
    # Sri Lankan country code
    COUNTRY_CODE = '94'
    
    # Pattern for Sri Lankan mobile numbers (7X followed by 7 digits)
    # Mobile: 70, 71, 72, 74, 75, 76, 77, 78
    MOBILE_PATTERN = r'^(\+?94|0)?7[0-8]\d{7}$'
    
    # Pattern for landline numbers (various area codes)
    LANDLINE_PATTERN = r'^(\+?94|0)?(11|21|23|24|25|26|27|31|32|33|34|35|36|37|38|41|45|47|51|52|54|55|57|63|65|66|67|81|91)\d{7}$'
    
    # Check if it matches mobile or landline pattern
    is_mobile = bool(re.match(MOBILE_PATTERN, phone))
    is_landline = bool(re.match(LANDLINE_PATTERN, phone))
    
    if not (is_mobile or is_landline):
        raise ValidationError(
            "Enter a valid Sri Lankan phone number. "
            "Mobile: 07X-XXXXXXX or Landline: 0XX-XXXXXXX"
        )
    
    # Normalize to E.164 format (+94XXXXXXXXX)
    if phone.startswith('+94'):
        # Already in international format with +
        normalized = phone
    elif phone.startswith('94'):
        # International format without +
        normalized = '+' + phone
    elif phone.startswith('0'):
        # Local format, remove leading 0 and add country code
        normalized = '+' + COUNTRY_CODE + phone[1:]
    else:
        # Assume it's a local number without leading 0
        normalized = '+' + COUNTRY_CODE + phone
    
    # Final validation: should be +94 followed by 9 digits
    if not re.match(r'^\+94\d{9}$', normalized):
        raise ValidationError("Invalid Sri Lankan phone number format")
    
    return normalized


def normalize_sri_lankan_phone(phone):
    """
    Normalize Sri Lankan phone number to E.164 format
    This is a helper function that can be used in serializers and managers
    Raises ValidationError if phone is invalid
    """
    if not phone:
        raise ValidationError("Phone number is required")
    
    return validate_sri_lankan_phone_number(phone)

