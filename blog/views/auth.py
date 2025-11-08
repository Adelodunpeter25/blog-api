"""Authentication views."""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from blog.serializers import UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def google_auth(request):
    """Handle Google OAuth authentication."""
    google_token = request.data.get('access_token')
    
    if not google_token:
        return Response(
            {'error': 'Google access token is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Verify Google token and get user info
        import requests
        google_response = requests.get(
            f'https://www.googleapis.com/oauth2/v1/userinfo?access_token={google_token}'
        )
        
        if google_response.status_code != 200:
            return Response(
                {'error': 'Invalid Google token'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        google_data = google_response.json()
        email = google_data.get('email')
        name = google_data.get('name', '')
        google_id = google_data.get('id')
        
        if not email:
            return Response(
                {'error': 'Email not provided by Google'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Create new user
            username = email.split('@')[0]
            # Ensure unique username
            counter = 1
            original_username = username
            while User.objects.filter(username=username).exists():
                username = f"{original_username}{counter}"
                counter += 1
            
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=name.split(' ')[0] if name else '',
                last_name=' '.join(name.split(' ')[1:]) if len(name.split(' ')) > 1 else ''
            )
        
        # Create or get social account
        social_account, created = SocialAccount.objects.get_or_create(
            user=user,
            provider='google',
            defaults={'uid': google_id}
        )
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        
        # Serialize user data
        user_serializer = UserSerializer(user, context={'request': request})
        
        return Response({
            'access_token': str(access_token),
            'refresh_token': str(refresh),
            'user': user_serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': 'Authentication failed'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Login with email and password."""
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response(
            {'error': 'Email and password are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            # Serialize user data
            user_serializer = UserSerializer(user, context={'request': request})
            
            return Response({
                'access_token': str(access_token),
                'refresh_token': str(refresh),
                'user': user_serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    except User.DoesNotExist:
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """Register new user with email and password."""
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')
    
    if not email or not password:
        return Response(
            {'error': 'Email and password are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(email=email).exists():
        return Response(
            {'error': 'User with this email already exists'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create username from email
    username = email.split('@')[0]
    counter = 1
    original_username = username
    while User.objects.filter(username=username).exists():
        username = f"{original_username}{counter}"
        counter += 1
    
    # Create user
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    
    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    
    # Serialize user data
    user_serializer = UserSerializer(user, context={'request': request})
    
    return Response({
        'access_token': str(access_token),
        'refresh_token': str(refresh),
        'user': user_serializer.data
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    """Logout user by blacklisting refresh token."""
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
    except Exception:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)