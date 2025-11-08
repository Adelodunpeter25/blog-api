"""Test cases for blog serializers."""

from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Category, Tag, Post, Comment
from blog.serializers import (
    CategorySerializer, TagSerializer, PostListSerializer, 
    PostDetailSerializer, PostCreateUpdateSerializer, CommentSerializer
)


class SerializerTest(TestCase):
    """Test blog serializers."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.category = Category.objects.create(
            name="Technology",
            description="Tech posts"
        )
        self.tag = Tag.objects.create(name="Python")
        
        self.post = Post.objects.create(
            title="Test Post",
            content="This is a test post with enough content to test read time calculation. " * 10,
            author=self.user,
            category=self.category,
            status="published"
        )
        self.post.tags.add(self.tag)
        
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content="Great post!",
            is_approved=True
        )
    
    def test_category_serializer(self):
        """Test CategorySerializer."""
        serializer = CategorySerializer(self.category)
        data = serializer.data
        
        self.assertEqual(data['name'], "Technology")
        self.assertEqual(data['slug'], "technology")
        self.assertEqual(data['description'], "Tech posts")
    
    def test_tag_serializer(self):
        """Test TagSerializer."""
        serializer = TagSerializer(self.tag)
        data = serializer.data
        
        self.assertEqual(data['name'], "Python")
        self.assertEqual(data['slug'], "python")
    
    def test_post_list_serializer(self):
        """Test PostListSerializer includes excerpt and read time."""
        serializer = PostListSerializer(self.post)
        data = serializer.data
        
        self.assertEqual(data['title'], "Test Post")
        self.assertEqual(data['author_name'], "testuser")
        self.assertIn('excerpt', data)
        self.assertIn('read_time', data)
        self.assertIn('category', data)
        self.assertIn('tags', data)
    
    def test_post_detail_serializer(self):
        """Test PostDetailSerializer includes full content and comments."""
        serializer = PostDetailSerializer(self.post)
        data = serializer.data
        
        self.assertEqual(data['title'], "Test Post")
        self.assertIn('content', data)
        self.assertIn('comments', data)
        self.assertIn('comment_count', data)
        self.assertEqual(data['comment_count'], 1)
    
    def test_post_create_serializer_validation(self):
        """Test PostCreateUpdateSerializer validation."""
        # Valid data
        valid_data = {
            'title': 'Valid Title',
            'content': 'Valid content with enough characters',
            'status': 'draft'
        }
        serializer = PostCreateUpdateSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        
        # Invalid title (too short)
        invalid_data = {
            'title': 'Hi',
            'content': 'Valid content',
            'status': 'draft'
        }
        serializer = PostCreateUpdateSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
    
    def test_comment_serializer(self):
        """Test CommentSerializer shows author name."""
        serializer = CommentSerializer(self.comment)
        data = serializer.data
        
        self.assertEqual(data['content'], "Great post!")
        self.assertEqual(data['author_name'], "testuser")
        self.assertTrue(data['is_approved'])
    
    def test_comment_serializer_anonymous(self):
        """Test CommentSerializer with anonymous comment."""
        anon_comment = Comment.objects.create(
            post=self.post,
            email="anon@example.com",
            content="Anonymous comment"
        )
        
        serializer = CommentSerializer(anon_comment)
        data = serializer.data
        
        self.assertEqual(data['author_name'], "anon@example.com")
        self.assertEqual(data['email'], "anon@example.com")