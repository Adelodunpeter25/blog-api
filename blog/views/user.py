"""User and profile viewsets."""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import F
from blog.models import UserProfile, Follow
from blog.serializers import UserSerializer, UserProfileSerializer, FollowSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """User viewset with profile and follow functionality."""
    
    queryset = User.objects.all().select_related('profile')
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    
    @action(detail=True, methods=['post', 'delete'], permission_classes=[permissions.IsAuthenticated])
    def follow(self, request, pk=None):
        """Follow or unfollow a user."""
        user_to_follow = self.get_object()
        
        if user_to_follow == request.user:
            return Response(
                {'error': 'Cannot follow yourself'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        follow_obj, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )
        
        if request.method == 'POST':
            if not created:
                return Response(
                    {'error': 'Already following this user'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Update follower counts
            user_to_follow.profile.follower_count = F('follower_count') + 1
            user_to_follow.profile.save()
            request.user.profile.following_count = F('following_count') + 1
            request.user.profile.save()
            
            return Response({'status': 'following'}, status=status.HTTP_201_CREATED)
        
        elif request.method == 'DELETE':
            if created:
                follow_obj.delete()
            
            deleted_count, _ = Follow.objects.filter(
                follower=request.user,
                following=user_to_follow
            ).delete()
            
            if deleted_count:
                # Update follower counts
                user_to_follow.profile.follower_count = F('follower_count') - 1
                user_to_follow.profile.save()
                request.user.profile.following_count = F('following_count') - 1
                request.user.profile.save()
                
                return Response({'status': 'unfollowed'}, status=status.HTTP_200_OK)
            
            return Response(
                {'error': 'Not following this user'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        """Get user's followers."""
        user = self.get_object()
        followers = Follow.objects.filter(following=user).select_related('follower__profile')
        serializer = FollowSerializer(followers, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def following(self, request, pk=None):
        """Get users that this user is following."""
        user = self.get_object()
        following = Follow.objects.filter(follower=user).select_related('following__profile')
        serializer = FollowSerializer(following, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get', 'put'], permission_classes=[permissions.IsAuthenticated])
    def profile(self, request):
        """Get or update current user's profile."""
        if request.method == 'GET':
            serializer = UserSerializer(request.user, context={'request': request})
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            # Update user fields
            user_serializer = UserSerializer(
                request.user, 
                data=request.data, 
                partial=True,
                context={'request': request}
            )
            
            # Update profile fields
            profile_serializer = UserProfileSerializer(
                request.user.profile,
                data=request.data,
                partial=True
            )
            
            if user_serializer.is_valid() and profile_serializer.is_valid():
                user_serializer.save()
                profile_serializer.save()
                return Response(user_serializer.data)
            
            errors = {}
            errors.update(user_serializer.errors)
            errors.update(profile_serializer.errors)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)