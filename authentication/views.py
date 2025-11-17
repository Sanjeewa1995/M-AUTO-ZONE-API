from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging
from django.db import IntegrityError
from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    UserUpdateSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    OTPVerificationSerializer,
    ChangePasswordSerializer
)
from common.utils import APIResponse


class RegisterView(generics.CreateAPIView):
    """
    Register a new user
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse.validation_error(serializer.errors)

        try:
            user = serializer.save()
        except IntegrityError as exc:
            error_message = str(exc).lower()
            if 'users.phone' in error_message:
                return APIResponse.error(
                    message='Phone number already exists',
                    error_code='DUPLICATE_PHONE',
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            if 'users.email' in error_message:
                return APIResponse.error(
                    message='Email already exists',
                    error_code='DUPLICATE_EMAIL',
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            logger = logging.getLogger(__name__)
            logger.error(f'User registration integrity error: {exc}', exc_info=True)
            return APIResponse.error(
                message='Unable to complete registration. Please try again.',
                error_code='REGISTRATION_FAILED',
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Generate tokens for the new user
        refresh = RefreshToken.for_user(user)

        response_data = {
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            },
            'user': UserSerializer(user).data
        }

        return APIResponse.success(
            data=response_data,
            message='User registered successfully',
            status_code=status.HTTP_201_CREATED
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login user and return JWT tokens
    """
    serializer = UserLoginSerializer(data=request.data)
    if not serializer.is_valid():
        return APIResponse.validation_error(serializer.errors)

    user = serializer.validated_data['user']
    refresh = RefreshToken.for_user(user)

    response_data = {
        'tokens': {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        },
        'user': UserSerializer(user).data
    }

    return APIResponse.success(
        data=response_data,
        message='Login successful'
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout user by blacklisting the refresh token
    """
    # Check if refresh token is provided
    if 'refresh' not in request.data or not request.data.get('refresh'):
        return APIResponse.error(
            message='Refresh token is required',
            error_code='REFRESH_TOKEN_REQUIRED',
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return APIResponse.success(message='Logout successful')
    except (KeyError, TypeError):
        return APIResponse.error(
            message='Refresh token is required',
            error_code='REFRESH_TOKEN_REQUIRED',
            status_code=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        # Handle token errors (invalid, expired, already blacklisted, etc.)
        error_message = str(e).lower()
        if 'token' in error_message or 'invalid' in error_message or 'expired' in error_message or 'blacklist' in error_message:
            return APIResponse.error(
                message='Invalid or expired refresh token. Please login again.',
                error_code='INVALID_TOKEN',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        # Log the actual error for debugging
        logger = logging.getLogger(__name__)
        logger.error(f'Logout error: {str(e)}', exc_info=True)
        return APIResponse.error(
            message='Logout failed. Please try again.',
            error_code='LOGOUT_FAILED',
            status_code=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
    """
    Get current user profile
    """
    serializer = UserSerializer(request.user)
    return APIResponse.success(
        data=serializer.data,
        message='Profile retrieved successfully'
    )


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile_view(request):
    """
    Update current user profile
    """
    serializer = UserUpdateSerializer(
        request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        # Return updated user data
        user_serializer = UserSerializer(request.user)
        return APIResponse.success(
            data={'user': user_serializer.data},
            message='Profile updated successfully'
        )
    return APIResponse.validation_error(serializer.errors)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token_view(request):
    """
    Refresh JWT access token
    """
    # Check if refresh token is provided
    if 'refresh' not in request.data or not request.data.get('refresh'):
        return APIResponse.error(
            message='Refresh token is required',
            error_code='REFRESH_TOKEN_REQUIRED',
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        refresh_token = request.data['refresh']
        token = RefreshToken(refresh_token)
        return APIResponse.success(
            data={'access': str(token.access_token)},
            message='Token refreshed successfully'
        )
    except (KeyError, TypeError):
        return APIResponse.error(
            message='Refresh token is required',
            error_code='REFRESH_TOKEN_REQUIRED',
            status_code=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        # Handle token errors (invalid, expired, already blacklisted, etc.)
        error_message = str(e).lower()
        if 'token' in error_message or 'invalid' in error_message or 'expired' in error_message or 'blacklist' in error_message:
            return APIResponse.error(
                message='Invalid or expired refresh token. Please login again.',
                error_code='INVALID_REFRESH_TOKEN',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        # Log the actual error for debugging
        logger = logging.getLogger(__name__)
        logger.error(f'Token refresh error: {str(e)}', exc_info=True)
        return APIResponse.error(
            message='Token refresh failed. Please try again.',
            error_code='REFRESH_FAILED',
            status_code=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request_view(request):
    """
    Request password reset - send OTP via email or SMS
    """
    serializer = PasswordResetRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return APIResponse.validation_error(serializer.errors)

    phone = serializer.validated_data['phone']

    try:
        user = User.objects.get(phone=phone)
        # Generate OTP
        otp = user.generate_reset_otp()

        # Send OTP via email if email exists, otherwise log for SMS (you can integrate SMS service here)
        if user.email:
            # Send OTP email
            subject = 'Password Reset OTP - Vehicle Parts API'

            # Simple email template
            html_message = f"""
            <html>
            <body>
                <h2>Password Reset OTP</h2>
                <p>Hello {user.first_name},</p>
                <p>You have requested to reset your password for the Vehicle Parts API.</p>
                <p>Your OTP is: <strong style="font-size: 24px; color: #007bff;">{otp}</strong></p>
                <p>This OTP will expire in 10 minutes.</p>
                <p>If you did not request this password reset, please ignore this email.</p>
                <br>
                <p>Best regards,<br>Vehicle Parts API Team</p>
            </body>
            </html>
            """
            plain_message = f"""
            Password Reset OTP
            
            Hello {user.first_name},
            
            You have requested to reset your password for the Vehicle Parts API.
            
            Your OTP is: {otp}
            
            This OTP will expire in 10 minutes.
            
            If you did not request this password reset, please ignore this email.
            
            Best regards,
            Vehicle Parts API Team
            """

            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            # TODO: Integrate SMS service here to send OTP via WhatsApp/SMS
            logger = logging.getLogger(__name__)
            logger.info(f'Password reset OTP {otp} generated for user {user.phone}. Email sent to {user.email}')

        return APIResponse.success(
            data={
                'phone': phone,
                'expires_in': '10 minutes',
                'method': 'email' if user.email else 'sms'
            },
            message='Password reset OTP sent successfully'
        )

    except User.DoesNotExist:
        # Don't reveal if phone exists or not for security
        return APIResponse.success(
            data={'phone': phone},
            message='If an account with this phone number exists, a password reset OTP has been sent'
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm_view(request):
    """
    Confirm password reset with OTP
    """
    serializer = PasswordResetConfirmSerializer(data=request.data)
    if not serializer.is_valid():
        return APIResponse.validation_error(serializer.errors)

    phone = serializer.validated_data['phone']
    otp = serializer.validated_data['otp']
    new_password = serializer.validated_data['new_password']

    try:
        user = User.objects.get(phone=phone)

        # Validate OTP
        is_valid, message = user.is_otp_valid(otp)
        if not is_valid:
            return APIResponse.error(
                message=message,
                error_code='INVALID_OTP'
            )

        # Set new password
        user.set_password(new_password)
        user.clear_reset_otp()  # Clear the OTP
        user.save()

        return APIResponse.success(
            message='Password reset successfully'
        )

    except User.DoesNotExist:
        return APIResponse.not_found(
            message='User not found',
            resource_type='User'
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp_view(request):
    """
    Verify OTP without resetting password
    """
    serializer = OTPVerificationSerializer(data=request.data)
    if not serializer.is_valid():
        return APIResponse.validation_error(serializer.errors)

    phone = serializer.validated_data['phone']
    otp = serializer.validated_data['otp']

    try:
        user = User.objects.get(phone=phone)

        # Validate OTP
        is_valid, message = user.is_otp_valid(otp)
        if not is_valid:
            return APIResponse.error(
                message=message,
                error_code='INVALID_OTP'
            )

        return APIResponse.success(
            data={'phone': phone},
            message='OTP verified successfully'
        )

    except User.DoesNotExist:
        return APIResponse.not_found(
            message='User not found',
            resource_type='User'
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """
    Change password for authenticated user
    """
    serializer = ChangePasswordSerializer(
        data=request.data, context={'request': request})
    if not serializer.is_valid():
        return APIResponse.validation_error(serializer.errors)

    user = request.user
    new_password = serializer.validated_data['new_password']

    # Set new password
    user.set_password(new_password)
    user.save()

    return APIResponse.success(
        message='Password changed successfully'
    )
