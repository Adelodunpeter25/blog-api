"""User and profile serializers."""

from rest_framework import serializers
from django.contrib.auth.models import User
from blog.models import UserProfile, Follow


class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer."""
    
    avatar_thumbnail = serializers.SerializerMethodField()
    avatar_small = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = [
            'bio', 'avatar', 'avatar_thumbnail', 'avatar_small',
            'website', 'twitter', 'github', 'linkedin', 
            'follower_count', 'following_count'
        ]
    
    def get_avatar_thumbnail(self, obj):
        """Get avatar thumbnail URL."""
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar_thumbnail.url)
        return None
    
    def get_avatar_small(self, obj):
        """Get small avatar URL."""
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar_small.url)
        return None


class UserSerializer(serializers.ModelSerializer):
    """User serializer with profile data."""
    
    profile = UserProfileSerializer(read_only=True)
    is_following = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'date_joined', 'profile', 'is_following'
        ]
        read_only_fields = ['id', 'date_joined']
    
    def get_is_following(self, obj):
        """Check if current user is following this user."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Follow.objects.filter(
                follower=request.user, 
                following=obj
            ).exists()
        return False


class FollowSerializer(serializers.ModelSerializer):
    """Follow relationship serializer."""
    
    follower = UserSerializer(read_only=True)
    following = UserSerializer(read_only=True)
    
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']
        read_only_fields = ['id', 'created_at']