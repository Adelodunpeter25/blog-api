"""Comment viewsets."""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from blog.models import Comment, Post
from blog.serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for comments with approval system."""
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action in ['approve', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Filter comments by post if specified."""
        queryset = Comment.objects.all()
        post_slug = self.request.query_params.get('post', None)
        if post_slug:
            queryset = queryset.filter(post__slug=post_slug)
        
        # Only show approved comments to non-admin users
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_approved=True)
        
        return queryset.select_related('post', 'author')
    
    def perform_create(self, serializer):
        """Set author or email when creating comment."""
        post_slug = self.request.data.get('post_slug')
        try:
            post = Post.objects.get(slug=post_slug)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if self.request.user.is_authenticated:
            serializer.save(post=post, author=self.request.user)
        else:
            email = self.request.data.get('email')
            if not email:
                return Response({'error': 'Email required for anonymous comments'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            serializer.save(post=post, email=email)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        """Approve a comment (admin only)."""
        comment = self.get_object()
        comment.is_approved = True
        comment.save()
        return Response({'status': 'comment approved'})