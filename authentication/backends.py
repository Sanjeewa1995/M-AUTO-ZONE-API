from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError

from .validators import validate_sri_lankan_phone_number


class PhoneNormalizingModelBackend(ModelBackend):
    """
    Authenticates using the phone number (USERNAME_FIELD), normalizing it to
    E.164 first so local formats (0771234567) match the stored +947...
    format. Needed for Django admin login, which calls authenticate()
    directly without going through UserLoginSerializer's normalization.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username:
            try:
                username = validate_sri_lankan_phone_number(username)
            except ValidationError:
                return None
        return super().authenticate(request, username=username, password=password, **kwargs)
