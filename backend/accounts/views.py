"""
Accounts Views - Register, Login, Profile, Leaderboard
"""
from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile, Badge
from .serializers import (
    UserRegistrationSerializer, UserProfileSerializer,
    LeaderboardUserSerializer, BadgeSerializer
)


class RegisterView(generics.CreateAPIView):
    """POST /api/accounts/register/ - Create new user account."""
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens for the new user
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Account created successfully! Welcome to EduPlay 🎮',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """POST /api/accounts/login/ - Login and receive JWT tokens."""
    from django.contrib.auth import authenticate
    username = request.data.get('username', '')
    password = request.data.get('password', '')

    # Allow login with email as well
    if '@' in username:
        try:
            user_obj = User.objects.get(email=username)
            username = user_obj.username
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)

    # Update last active on login
    from django.utils import timezone
    profile = user.profile
    profile.last_active = timezone.now().date()
    profile.save()

    refresh = RefreshToken.for_user(user)
    return Response({
        'message': f'Welcome back, {user.first_name or user.username}! 🎉',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'xp_points': profile.xp_points,
            'level': profile.level,
        },
        'tokens': {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
    })


class ProfileView(generics.RetrieveUpdateAPIView):
    """GET/PUT /api/accounts/profile/ - Get or update logged-in user's profile."""
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user.profile


class LeaderboardView(generics.ListAPIView):
    """GET /api/accounts/leaderboard/ - Top users by XP."""
    permission_classes = [AllowAny]
    serializer_class = LeaderboardUserSerializer

    def get_queryset(self):
        return UserProfile.objects.select_related('user').order_by('-xp_points')[:20]


class BadgeListView(generics.ListAPIView):
    """GET /api/accounts/badges/ - List all available badges."""
    permission_classes = [AllowAny]
    serializer_class = BadgeSerializer
    queryset = Badge.objects.all()
