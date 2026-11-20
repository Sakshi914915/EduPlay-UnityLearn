"""
EduPlay - Main URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import api_root

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # Root Directory & API Directory
    path('', api_root, name='platform-root'),
    path('api/', api_root, name='api-root'),

    # JWT Auth Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 6 Module App Endpoints
    path('api/accounts/', include('accounts.urls')),
    path('api/gamebased/', include('gamebased.urls')),
    path('api/simulations/', include('simulations.urls')),
    path('api/learningpaths/', include('learningpaths.urls')),
    path('api/collaborative/', include('collaborative.urls')),
    path('api/analytics/', include('analytics.urls')),
    path('api/authoring/', include('authoring.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
