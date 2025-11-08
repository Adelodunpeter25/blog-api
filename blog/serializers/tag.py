"""Tag serializers."""

from rest_framework import serializers
from blog.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Simple serializer for tags."""
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']