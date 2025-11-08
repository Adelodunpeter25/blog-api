"""Test cases for blog views."""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from blog.models import Category, Tag, Post, Comment


class PostViewSetTest(TestCase):
    """Test PostViewSet endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com", 
            password="admin123"
        )
        self.category = Category.objects.create(name="Tech")
        self.tag = Tag.objects.create(name="Python")
        
        self.published_post = Post.objects.create(
            title="Published Post",
            content="This is published content",
            author=self.user,
            category=self.category,
            status="published"
        )
        self.published_post.tags.add(self.tag)
        
        self.draft_post = Post.objects.create(
            title="Draft Post", 
            content="This is draft content",
            author=self.user,
            status="draft"
        )
    
    def test_list_posts_anonymous(self):
        """Test listing posts as anonymous user."""
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Only published posts
        self.assertEqual(response.data['results'][0]['title'], "Published Post")
    
    def test_retrieve_post_increments_views(self):
        """Test retrieving post increments view count."""
        initial_views = self.published_post.views_count
        response = self.client.get(f'/api/posts/{self.published_post.slug}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.published_post.refresh_from_db()
        self.assertEqual(self.published_post.views_count, initial_views + 1)
    
    def test_create_post_authenticated(self):
        """Test creating post as authenticated user."""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Post',
            'content': 'New content',
            'category': self.category.id,
            'status': 'published'
        }
        response = self.client.post('/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 3)
    
    def test_create_post_anonymous_forbidden(self):
        """Test creating post as anonymous user is forbidden."""
        data = {
            'title': 'New Post',
            'content': 'New content'
        }
        response = self.client.post('/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_own_post(self):
        """Test updating own post."""
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Updated Title'}
        response = self.client.patch(f'/api/posts/{self.published_post.slug}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.published_post.refresh_from_db()
        self.assertEqual(self.published_post.title, 'Updated Title')
    
    def test_update_other_post_forbidden(self):
        """Test updating other user's post is forbidden."""
        other_user = User.objects.create_user(username="other", password="pass")
        self.client.force_authenticate(user=other_user)
        
        data = {'title': 'Hacked Title'}
        response = self.client.patch(f'/api/posts/{self.published_post.slug}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_my_posts_endpoint(self):
        """Test my_posts custom action."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/posts/my_posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both published and draft
    
    def test_statistics_endpoint(self):
        """Test statistics custom action."""
        response = self.client.get('/api/posts/statistics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_posts', response.data)
        self.assertIn('total_views', response.data)
        self.assertIn('most_viewed_post', response.data)
    
    def test_search_posts(self):
        """Test searching posts."""
        response = self.client.get('/api/posts/?search=published')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_filter_by_category(self):
        """Test filtering posts by category."""
        response = self.client.get(f'/api/posts/?category={self.category.slug}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class CommentViewSetTest(TestCase):
    """Test CommentViewSet endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.admin = User.objects.create_superuser(
            username="admin",
            password="admin123"
        )
        self.post = Post.objects.create(
            title="Test Post",
            content="Test content",
            author=self.user,
            status="published"
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content="Test comment",
            is_approved=True
        )
    
    def test_create_comment_authenticated(self):
        """Test creating comment as authenticated user."""
        self.client.force_authenticate(user=self.user)
        data = {
            'post_slug': self.post.slug,
            'content': 'New comment'
        }
        response = self.client.post('/api/comments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_anonymous_comment(self):
        """Test creating anonymous comment with email."""
        data = {
            'post_slug': self.post.slug,
            'content': 'Anonymous comment',
            'email': 'anon@example.com'
        }
        response = self.client.post('/api/comments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_approve_comment_admin(self):
        """Test approving comment as admin."""
        unapproved_comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content="Unapproved comment",
            is_approved=False
        )
        
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(f'/api/comments/{unapproved_comment.id}/approve/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        unapproved_comment.refresh_from_db()
        self.assertTrue(unapproved_comment.is_approved)
    
    def test_approve_comment_non_admin_forbidden(self):
        """Test approving comment as non-admin is forbidden."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/api/comments/{self.comment.id}/approve/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)