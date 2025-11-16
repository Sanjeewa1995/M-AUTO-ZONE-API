from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator
import uuid
from django.utils import timezone
from .validators import validate_sri_lankan_phone_number, normalize_sri_lankan_phone


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone number field must be set')
        # Normalize Sri Lankan phone number to E.164 format
        phone = normalize_sri_lankan_phone(phone)
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model with essential fields only
    """
    # Remove username field and use phone number as unique identifier
    username = None
    email = models.EmailField(blank=True, null=True, help_text="Optional email address")
    
    # Use custom manager
    objects = UserManager()
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(
        max_length=15,
        unique=True,
        validators=[validate_sri_lankan_phone_number],
        help_text="Sri Lankan phone number used for login (E.164 format: +94771234567 or local: 0771234567)"
    )
    
    # User type choices
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
        ('moderator', 'Moderator'),
    ]
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='user'
    )
    
    # Override is_active to make it explicit
    is_active = models.BooleanField(default=True)
    
    # Password reset OTP fields
    reset_otp = models.CharField(max_length=6, null=True, blank=True)
    reset_otp_expires = models.DateTimeField(null=True, blank=True)
    otp_attempts = models.IntegerField(default=0)
    otp_locked_until = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Use phone number as the username field
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        email_part = f" - {self.email}" if self.email else ""
        return f"{self.phone}{email_part} ({self.get_full_name()})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_short_name(self):
        return self.first_name
    
    def generate_reset_otp(self):
        """Generate a new 6-digit OTP and set expiration"""
        import random
        self.reset_otp = str(random.randint(100000, 999999))
        self.reset_otp_expires = timezone.now() + timezone.timedelta(minutes=10)  # OTP expires in 10 minutes
        self.otp_attempts = 0
        self.otp_locked_until = None
        self.save(update_fields=['reset_otp', 'reset_otp_expires', 'otp_attempts', 'otp_locked_until'])
        return self.reset_otp
    
    def is_otp_valid(self, otp):
        """Check if the OTP is valid and not expired"""
        if self.otp_locked_until and timezone.now() < self.otp_locked_until:
            return False, "Account is temporarily locked due to too many failed attempts"
        
        if not self.reset_otp or not self.reset_otp_expires:
            return False, "No OTP found"
        
        if timezone.now() > self.reset_otp_expires:
            return False, "OTP has expired"
        
        if self.reset_otp != otp:
            # Increment failed attempts
            self.otp_attempts += 1
            if self.otp_attempts >= 3:  # Lock after 3 failed attempts
                self.otp_locked_until = timezone.now() + timezone.timedelta(minutes=15)
            self.save(update_fields=['otp_attempts', 'otp_locked_until'])
            return False, "Invalid OTP"
        
        return True, "OTP is valid"
    
    def clear_reset_otp(self):
        """Clear the OTP after successful password reset"""
        self.reset_otp = None
        self.reset_otp_expires = None
        self.otp_attempts = 0
        self.otp_locked_until = None
        self.save(update_fields=['reset_otp', 'reset_otp_expires', 'otp_attempts', 'otp_locked_until'])