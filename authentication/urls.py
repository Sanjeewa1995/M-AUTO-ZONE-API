from django.urls import path
from .views import (
    RegisterView,
    login_view,
    logout_view,
    user_profile_view,
    update_profile_view,
    refresh_token_view
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', user_profile_view, name='user-profile'),
    path('profile/update/', update_profile_view, name='update-profile'),
    path('refresh/', refresh_token_view, name='refresh-token'),
]
