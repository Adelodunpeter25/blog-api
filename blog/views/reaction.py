"""Reaction and reading list viewsets."""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from blog.models import Post, Reaction, ReadingList
from blog.serializers import ReactionSerializer, ReadingListSerializer


class ReactionViewSet(viewsets.ViewSet):
    """ViewSet for post reactions."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['post'], url_path='react')
    def react_to_post(self, request):
        """Add or remove reaction to a post."""
        post_slug = request.data.get('post_slug')
        reaction_type = request.data.get('reaction_type')
        
        if not post_slug or not reaction_type:
            return Response(
                {'error': 'post_slug and reaction_type are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if reaction_type not in ['like', 'love', 'bookmark']:
            return Response(
                {'error': 'Invalid reaction type'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        post = get_object_or_404(Post, slug=post_slug, status='published')
        
        # Check if reaction already exists
        reaction, created = Reaction.objects.get_or_create(
            user=request.user,
            post=post,
            reaction_type=reaction_type
        )
        
        if not created:
            # Remove existing reaction
            reaction.delete()
            return Response({'status': 'removed'}, status=status.HTTP_200_OK)
        
        serializer = ReactionSerializer(reaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReadingListViewSet(viewsets.ViewSet):
    """ViewSet for user's reading list."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        """Get user's reading list."""
        reading_list = ReadingList.objects.filter(user=request.user).select_related('post')
        serializer = ReadingListSerializer(reading_list, many=True, context={'request': request})
        return Response(serializer.data)
    
    def create(self, request):
        """Add post to reading list."""
        post_slug = request.data.get('post_slug')
        
        if not post_slug:
            return Response(
                {'error': 'post_slug is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        post = get_object_or_404(Post, slug=post_slug, status='published')
        
        reading_item, created = ReadingList.objects.get_or_create(
            user=request.user,
            post=post
        )
        
        if not created:
            return Response(
                {'error': 'Post already in reading list'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ReadingListSerializer(reading_item, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk=None):
        """Remove post from reading list."""
        try:
            post = Post.objects.get(slug=pk, status='published')
            reading_item = ReadingList.objects.get(user=request.user, post=post)
            reading_item.delete()
            return Response({'status': 'removed'}, status=status.HTTP_200_OK)
        except (Post.DoesNotExist, ReadingList.DoesNotExist):
            return Response(
                {'error': 'Post not found in reading list'}, 
                status=status.HTTP_404_NOT_FOUND
            )