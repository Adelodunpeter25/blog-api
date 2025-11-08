"""Image validation utilities."""

from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from PIL import Image
import os


def validate_image_size(image):
    """Validate image file size (max 5MB)."""
    max_size = 5 * 1024 * 1024  # 5MB
    if image.size > max_size:
        raise ValidationError('Image file too large. Maximum size is 5MB.')


def validate_image_dimensions(image):
    """Validate image dimensions (max 4000x4000)."""
    width, height = get_image_dimensions(image)
    max_dimension = 4000
    
    if width > max_dimension or height > max_dimension:
        raise ValidationError(f'Image dimensions too large. Maximum is {max_dimension}x{max_dimension}.')


def validate_image_format(image):
    """Validate image format (JPEG, PNG, WebP only)."""
    allowed_formats = ['JPEG', 'PNG', 'WEBP']
    
    try:
        with Image.open(image) as img:
            if img.format not in allowed_formats:
                raise ValidationError(f'Invalid image format. Allowed formats: {", ".join(allowed_formats)}')
    except Exception:
        raise ValidationError('Invalid image file.')


def validate_avatar_image(image):
    """Validate avatar image."""
    validate_image_size(image)
    validate_image_dimensions(image)
    validate_image_format(image)


def validate_featured_image(image):
    """Validate featured image."""
    validate_image_size(image)
    validate_image_dimensions(image)
    validate_image_format(image)