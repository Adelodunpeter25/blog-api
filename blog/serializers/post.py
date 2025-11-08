"""Post serializers."""

import math
from rest_framework import serializers
from blog.models import Post
from .category import CategorySerializer
from .tag import TagSerializer
from .comment import CommentSerializer


class PostListSerializer(serializers.ModelSerializer):
    """Minimal version for post list: title, slug, excerpt, author, category, tags, featured_image, created_at, view_count."""
    
    author_name = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    excerpt = serializers.SerializerMethodField()
    read_time = serializers.SerializerMethodField()
    reaction_counts = serializers.SerializerMethodField()
    user_reactions = serializers.SerializerMethodField()
    featured_image_urls = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'excerpt', 'author_name', 'category', 
            'tags', 'featured_image', 'featured_image_urls', 'created_at', 
            'views_count', 'read_time', 'reaction_counts', 'user_reactions'
        ]
    
    def get_author_name(self, obj):
        """Get author username."""
        return obj.author.username
    
    def get_excerpt(self, obj):
        """Get first 150 characters of content."""
        return obj.content[:150] + '...' if len(obj.content) > 150 else obj.content
    
    def get_read_time(self, obj):
        """Estimate read time based on word count (200 words per minute)."""
        word_count = len(obj.content.split())
        return max(1, math.ceil(word_count / 200))
    
    def get_reaction_counts(self, obj):
        """Get reaction counts for the post."""
        from django.db.models import Count
        reactions = obj.reactions.values('reaction_type').annotate(count=Count('reaction_type'))
        return {reaction['reaction_type']: reaction['count'] for reaction in reactions}
    
    def get_user_reactions(self, obj):
        """Get current user's reactions to this post."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user_reactions = obj.reactions.filter(user=request.user).values_list('reaction_type', flat=True)
            return list(user_reactions)
        return []
    
    def get_featured_image_urls(self, obj):
        """Get optimized featured image URLs."""
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return {
                    'large': request.build_absolute_uri(obj.featured_image_large.url),
                    'medium': request.build_absolute_uri(obj.featured_image_medium.url),
                    'small': request.build_absolute_uri(obj.featured_image_small.url),
                    'webp': request.build_absolute_uri(obj.featured_image_webp.url),
                }
        return None


class PostDetailSerializer(serializers.ModelSerializer):
    """Full version: includes full content, comments, and all fields."""
    
    author_name = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    read_time = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'content', 'author_name', 'category',
            'tags', 'featured_image', 'status', 'created_at', 'updated_at',
            'views_count', 'comments', 'comment_count', 'read_time'
        ]
    
    def get_author_name(self, obj):
        """Get author username."""
        return obj.author.username
    
    def get_comment_count(self, obj):
        """Get approved comment count."""
        return obj.comments.filter(is_approved=True).count()
    
    def get_read_time(self, obj):
        """Estimate read time based on word count (200 words per minute)."""
        word_count = len(obj.content.split())
        return max(1, math.ceil(word_count / 200))


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """Used when creating/editing posts, includes validation."""
    
    class Meta:
        model = Post
        fields = [
            'title', 'content', 'category', 'tags', 'featured_image', 'status'
        ]
    
    def validate_title(self, value):
        """Validate title is not empty and reasonable length."""
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value.strip()
    
    def validate_content(self, value):
        """Validate content is not empty."""
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Content must be at least 10 characters long.")
        return value.strip()