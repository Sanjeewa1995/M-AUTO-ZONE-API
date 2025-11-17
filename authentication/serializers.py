from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .validators import normalize_sri_lankan_phone, validate_sri_lankan_phone_number
from django.core.exceptions import ValidationError


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('phone', 'email', 'first_name', 'last_name', 'user_type', 'password', 'password_confirm')
    
    def validate_email(self, value):
        """Ensure email is unique when provided"""
        if value:
            email = value.strip().lower()
            if User.objects.filter(email__iexact=email).exists():
                raise serializers.ValidationError("Email already exists")
            return email
        return value
    
    def validate_phone(self, value):
        """Validate and normalize Sri Lankan phone number"""
        if not value:
            raise serializers.ValidationError("Phone number is required")
        try:
            return validate_sri_lankan_phone_number(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()
    
    def validate_phone(self, value):
        """Validate and normalize Sri Lankan phone number"""
        if not value:
            raise serializers.ValidationError("Phone number is required")
        try:
            return validate_sri_lankan_phone_number(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
    
    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')
        
        if phone and password:
            user = authenticate(username=phone, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include phone number and password')


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        # Only include these fields in API responses (excludes is_superuser, is_staff, etc.)
        fields = (
            'id', 'email', 'first_name', 'last_name', 'full_name', 
            'phone', 'user_type', 'is_active', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'is_active', 'created_at', 'updated_at')
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'user_type')
    
    def validate_phone(self, value):
        """Validate and normalize Sri Lankan phone number"""
        if value:  # Phone is optional in update
            try:
                return validate_sri_lankan_phone_number(value)
            except ValidationError as e:
                raise serializers.ValidationError(str(e))
        return value
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()


class PasswordResetRequestSerializer(serializers.Serializer):
    phone = serializers.CharField()
    
    def validate_phone(self, value):
        """Validate and normalize Sri Lankan phone number"""
        if not value:
            raise serializers.ValidationError("Phone number is required")
        try:
            return validate_sri_lankan_phone_number(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
    
    def validate(self, attrs):
        phone = attrs.get('phone')
        if not User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError("User with this phone number does not exist")
        return attrs


class PasswordResetConfirmSerializer(serializers.Serializer):
    phone = serializers.CharField()
    otp = serializers.CharField(max_length=6, min_length=6)
    new_password = serializers.CharField(min_length=8)
    new_password_confirm = serializers.CharField()
    
    def validate_phone(self, value):
        """Validate and normalize Sri Lankan phone number"""
        if not value:
            raise serializers.ValidationError("Phone number is required")
        try:
            return validate_sri_lankan_phone_number(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def validate_otp(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("OTP must be a 6-digit number")
        return value


class OTPVerificationSerializer(serializers.Serializer):
    phone = serializers.CharField()
    otp = serializers.CharField(max_length=6, min_length=6)
    
    def validate_phone(self, value):
        """Validate and normalize Sri Lankan phone number"""
        if not value:
            raise serializers.ValidationError("Phone number is required")
        try:
            return validate_sri_lankan_phone_number(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
    
    def validate_otp(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("OTP must be a 6-digit number")
        return value


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)
    new_password_confirm = serializers.CharField()
    
    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect")
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match")
        return attrs
