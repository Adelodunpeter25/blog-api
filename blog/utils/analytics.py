"""Analytics utilities for blog statistics."""

from django.db.models import Sum, Count
from blog.models import Post


def get_blog_statistics():
    """Get overall blog statistics."""
    stats = Post.objects.filter(status='published').aggregate(
        total_posts=Count('id'),
        total_views=Sum('views_count')
    )
    
    most_viewed = Post.objects.filter(status='published').order_by('-views_count').first()
    
    return {
        'total_posts': stats['total_posts'] or 0,
        'total_views': stats['total_views'] or 0,
        'most_viewed_post': {
            'title': most_viewed.title if most_viewed else None,
            'slug': most_viewed.slug if most_viewed else None,
            'views': most_viewed.views_count if most_viewed else 0
        }
    }