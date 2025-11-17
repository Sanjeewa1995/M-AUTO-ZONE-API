from django.urls import path
from .views import (
    RegisterView,
    login_view,
    logout_view,
    user_profile_view,
    update_profile_view,
    refresh_token_view,
    password_reset_request_view,
    password_reset_confirm_view,
    verify_otp_view,
    change_password_view,
    delete_account_view
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', user_profile_view, name='user-profile'),
    path('profile/update/', update_profile_view, name='update-profile'),
    path('refresh/', refresh_token_view, name='refresh-token'),
    path('password-reset/', password_reset_request_view, name='password-reset-request'),
    path('password-reset/confirm/', password_reset_confirm_view, name='password-reset-confirm'),
    path('verify-otp/', verify_otp_view, name='verify-otp'),
    path('change-password/', change_password_view, name='change-password'),
    path('delete-account/', delete_account_view, name='delete-account'),
]
