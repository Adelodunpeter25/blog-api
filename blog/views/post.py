"""Post viewsets."""

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F, Q
from blog.models import Post
from blog.serializers import PostListSerializer, PostDetailSerializer, PostCreateUpdateSerializer
from blog.utils import PostFilter, get_blog_statistics, get_blog_statistics


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    """Custom permission: author or admin can edit, others read-only."""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user or request.user.is_staff


class PostViewSet(viewsets.ModelViewSet):
    """Main viewset for posts with different actions."""
    
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PostFilter
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'views_count', 'title']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter posts based on user permissions."""
        queryset = Post.objects.select_related('author', 'category').prefetch_related('tags', 'comments')
        
        # Show only published posts to non-authenticated users
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='published')
        # Show all posts to admin, only own posts + published to authors
        elif not self.request.user.is_staff:
            queryset = queryset.filter(
                Q(status='published') | Q(author=self.request.user)
            )
        
        return queryset
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return PostListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        return PostDetailSerializer
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthorOrAdminOrReadOnly]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    def retrieve(self, request, *args, **kwargs):
        """Get single post by slug and increment view count."""
        instance = self.get_object()
        
        # Increment view count
        Post.objects.filter(slug=instance.slug).update(views_count=F('views_count') + 1)
        instance.refresh_from_db()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        """Set author when creating post."""
        serializer.save(author=self.request.user)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_posts(self, request):
        """Get current user's posts (including drafts)."""
        posts = Post.objects.filter(author=request.user).select_related('category').prefetch_related('tags')
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def statistics(self, request):
        """Get blog statistics - total posts, views, most viewed post."""
        stats = get_blog_statistics()
        return Response(stats)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def drafts(self, request):
        """Get current user's draft posts."""
        drafts = Post.objects.filter(author=request.user, status='draft')
        drafts = drafts.select_related('category').prefetch_related('tags')
        serializer = PostListSerializer(drafts, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def statistics(self, request):
        """Get blog statistics - total posts, views, most viewed post."""
        stats = get_blog_statistics()
        return Response(stats)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def drafts(self, request):
        """Get current user's draft posts."""
        if not request.user.is_staff and request.user != request.user:
            # Only show own drafts unless admin
            drafts = Post.objects.filter(author=request.user, status='draft')
        else:
            drafts = Post.objects.filter(status='draft')
        
        drafts = drafts.select_related('category').prefetch_related('tags')
        serializer = PostListSerializer(drafts, many=True, context={'request': request})
        return Response(serializer.data)