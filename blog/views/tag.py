"""Tag viewsets."""

from rest_framework import viewsets, permissions
from blog.models import Tag
from blog.serializers import TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for tags."""
    
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'