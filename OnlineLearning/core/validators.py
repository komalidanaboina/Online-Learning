from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


image_file_validator = FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])
document_file_validator = FileExtensionValidator(['pdf', 'doc', 'docx', 'ppt', 'pptx', 'zip'])
video_file_validator = FileExtensionValidator(['mp4', 'webm', 'mov'])


def validate_positive_decimal(value):
    if value < 0:
        raise ValidationError('Value cannot be negative.')


def validate_percentage(value):
    if value < 0 or value > 100:
        raise ValidationError('Percentage must be between 0 and 100.')
