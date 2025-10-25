#!/bin/bash

# Fix Deployment Script
# This script will update the deployed container with the correct configuration

echo "🔧 Fixing deployment configuration..."

# Update the main urls.py file
cat > /tmp/urls.py << 'EOF'
"""
URL configuration for vehicle_parts_api project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/requests/', include('request.urls')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
EOF

# Update the settings.py file to include request app
cat > /tmp/settings_update.py << 'EOF'
# Add this to INSTALLED_APPS if not present
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'storages',
    'authentication',
    'request',  # Our request app
]
EOF

echo "✅ Configuration files created"
echo "📋 Next steps:"
echo "1. Copy these files to your EC2 instance"
echo "2. Update the container with the new configuration"
echo "3. Restart the container"
