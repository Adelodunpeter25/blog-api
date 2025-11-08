"""Comment serializers."""

from rest_framework import serializers
from blog.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """Nested under posts, show author name, comment content, approval status."""
    
    author_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'author_name', 'email', 'content', 'is_approved', 'created_at']
        read_only_fields = ['is_approved', 'created_at']
    
    def get_author_name(self, obj):
        """Get author name or email for anonymous comments."""
        if obj.author:
            return obj.author.username
        return obj.email or 'Anonymous'