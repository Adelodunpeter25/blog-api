"""Image processing utilities."""

from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFill, ResizeToFit
from pilkit.processors import Transpose


@register.generator('blog:avatar_thumbnail')
class AvatarThumbnail(ImageSpec):
    """Generate avatar thumbnail (150x150)."""
    
    processors = [
        Transpose(),
        ResizeToFill(150, 150)
    ]
    format = 'JPEG'
    options = {'quality': 85}


@register.generator('blog:avatar_small')
class AvatarSmall(ImageSpec):
    """Generate small avatar (50x50)."""
    
    processors = [
        Transpose(),
        ResizeToFill(50, 50)
    ]
    format = 'JPEG'
    options = {'quality': 80}


@register.generator('blog:featured_image_large')
class FeaturedImageLarge(ImageSpec):
    """Generate large featured image (800x400)."""
    
    processors = [
        Transpose(),
        ResizeToFit(800, 400)
    ]
    format = 'JPEG'
    options = {'quality': 85}


@register.generator('blog:featured_image_medium')
class FeaturedImageMedium(ImageSpec):
    """Generate medium featured image (400x200)."""
    
    processors = [
        Transpose(),
        ResizeToFit(400, 200)
    ]
    format = 'JPEG'
    options = {'quality': 80}


@register.generator('blog:featured_image_small')
class FeaturedImageSmall(ImageSpec):
    """Generate small featured image (200x100)."""
    
    processors = [
        Transpose(),
        ResizeToFit(200, 100)
    ]
    format = 'JPEG'
    options = {'quality': 75}


@register.generator('blog:featured_image_webp')
class FeaturedImageWebP(ImageSpec):
    """Generate WebP version of featured image."""
    
    processors = [
        Transpose(),
        ResizeToFit(800, 400)
    ]
    format = 'WEBP'
    options = {'quality': 80}