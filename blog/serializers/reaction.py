"""Reaction and reading list serializers."""

from rest_framework import serializers
from blog.models import Reaction, ReadingList
from .post import PostListSerializer


class ReactionSerializer(serializers.ModelSerializer):
    """Reaction serializer."""
    
    class Meta:
        model = Reaction
        fields = ['id', 'reaction_type', 'created_at']
        read_only_fields = ['id', 'created_at']


class ReadingListSerializer(serializers.ModelSerializer):
    """Reading list serializer."""
    
    post = PostListSerializer(read_only=True)
    
    class Meta:
        model = ReadingList
        fields = ['id', 'post', 'added_at']
        read_only_fields = ['id', 'added_at']