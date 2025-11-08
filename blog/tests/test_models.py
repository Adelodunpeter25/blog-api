"""Test cases for blog models."""

from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Category, Tag, Post, Comment


class CategoryModelTest(TestCase):
    """Test Category model."""
    
    def test_category_creation(self):
        """Test category creation and slug generation."""
        category = Category.objects.create(
            name="Technology",
            description="Tech related posts"
        )
        self.assertEqual(category.name, "Technology")
        self.assertEqual(category.slug, "technology")
        self.assertEqual(str(category), "Technology")


class TagModelTest(TestCase):
    """Test Tag model."""
    
    def test_tag_creation(self):
        """Test tag creation and slug generation."""
        tag = Tag.objects.create(name="Python")
        self.assertEqual(tag.name, "Python")
        self.assertEqual(tag.slug, "python")
        self.assertEqual(str(tag), "Python")


class PostModelTest(TestCase):
    """Test Post model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.category = Category.objects.create(name="Tech")
    
    def test_post_creation(self):
        """Test post creation and slug generation."""
        post = Post.objects.create(
            title="Test Post",
            content="This is test content",
            author=self.user,
            category=self.category,
            status="published"
        )
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.slug, "test-post")
        self.assertEqual(post.status, "published")
        self.assertEqual(post.views_count, 0)
        self.assertEqual(str(post), "Test Post")


class CommentModelTest(TestCase):
    """Test Comment model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com", 
            password="testpass123"
        )
        self.post = Post.objects.create(
            title="Test Post",
            content="Test content",
            author=self.user,
            status="published"
        )
    
    def test_comment_creation(self):
        """Test comment creation."""
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content="Great post!"
        )
        self.assertEqual(comment.content, "Great post!")
        self.assertFalse(comment.is_approved)
        self.assertEqual(str(comment), f"Comment by {self.user.username} on {self.post.title}")
    
    def test_anonymous_comment(self):
        """Test anonymous comment with email."""
        comment = Comment.objects.create(
            post=self.post,
            email="anon@example.com",
            content="Anonymous comment"
        )
        self.assertEqual(comment.email, "anon@example.com")
        self.assertIsNone(comment.author)