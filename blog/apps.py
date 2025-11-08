"""Blog app configuration."""

from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Blog app config class."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
