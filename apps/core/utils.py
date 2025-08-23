"""
Core utilities for the project.
"""

import uuid
from django.utils.text import slugify


def generate_uuid():
    """Generate a unique UUID."""
    return uuid.uuid4()


def generate_unique_slug(instance, field_name, new_slug=None):
    """
    Generate a unique slug for a model instance.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(getattr(instance, field_name))

    # Get model class
    model_class = instance.__class__

    # Check if slug exists
    slug_exists = model_class.objects.filter(slug=slug).exists()

    if slug_exists:
        # If slug exists, add random string to the end
        new_slug = f"{slug}-{str(uuid.uuid4())[:8]}"
        return generate_unique_slug(instance, field_name, new_slug=new_slug)

    return slug
