"""Django admin configuration for blog app."""

from django.contrib import admin
from .models import Category, Tag, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin configuration."""
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag admin configuration."""
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Post admin configuration."""
    list_display = ['title', 'author', 'category', 'status', 'created_at', 'views_count']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment admin configuration."""
    list_display = ['post', 'author', 'email', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        """Approve selected comments."""
        queryset.update(is_approved=True)
    approve_comments.short_description = 'Approve selected comments'
