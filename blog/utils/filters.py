"""Filtering utilities for blog models."""

import django_filters
from blog.models import Post, Category, Tag


class PostFilter(django_filters.FilterSet):
    """Filter for Post model with category, author, and status filtering."""
    
    category = django_filters.CharFilter(field_name='category__slug', lookup_expr='exact')
    author = django_filters.CharFilter(field_name='author__username', lookup_expr='exact')
    status = django_filters.ChoiceFilter(choices=Post.STATUS_CHOICES)
    tag = django_filters.CharFilter(field_name='tags__slug', lookup_expr='exact')
    
    class Meta:
        model = Post
        fields = ['category', 'author', 'status', 'tag']