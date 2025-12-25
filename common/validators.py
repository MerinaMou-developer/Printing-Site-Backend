"""
Custom validators
"""
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from .constants import MAX_FILE_SIZE, MAX_IMAGE_SIZE, ALLOWED_DOCUMENT_EXTENSIONS, ALLOWED_IMAGE_EXTENSIONS


def validate_file_size(file, max_size=MAX_FILE_SIZE):
    """Validate file size"""
    if file.size > max_size:
        raise ValidationError(f'File size cannot exceed {max_size / (1024 * 1024):.0f}MB.')


def validate_image_size(image, max_size=MAX_IMAGE_SIZE):
    """Validate image size"""
    if image.size > max_size:
        raise ValidationError(f'Image size cannot exceed {max_size / (1024 * 1024):.0f}MB.')


def validate_file_extension(file, allowed_extensions=ALLOWED_DOCUMENT_EXTENSIONS):
    """Validate file extension"""
    file_extension = file.name.split('.')[-1].lower()
    if file_extension not in allowed_extensions:
        raise ValidationError(
            f'Invalid file format. Allowed: {", ".join(allowed_extensions)}'
        )


def validate_image_extension(image, allowed_extensions=ALLOWED_IMAGE_EXTENSIONS):
    """Validate image extension"""
    file_extension = image.name.split('.')[-1].lower()
    if file_extension not in allowed_extensions:
        raise ValidationError(
            f'Invalid image format. Allowed: {", ".join(allowed_extensions)}'
        )


def validate_image_dimensions(image, min_width=100, min_height=100):
    """Validate image dimensions"""
    try:
        width, height = get_image_dimensions(image)
        if width is None or height is None:
            raise ValidationError('Invalid image file.')
        if width < min_width or height < min_height:
            raise ValidationError(
                f'Image dimensions must be at least {min_width}x{min_height} pixels.'
            )
    except Exception as e:
        raise ValidationError(f'Unable to read image dimensions: {str(e)}')

