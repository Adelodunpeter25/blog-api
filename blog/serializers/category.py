"""Category serializers."""

from rest_framework import serializers
from blog.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Simple serializer for category list/detail."""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']