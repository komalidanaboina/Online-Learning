import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


phone_validator = RegexValidator(
    regex=r'^\+?[1-9]\d{7,14}$',
    message='Enter a valid international phone number.',
)


def validate_social_links(value):
    if not isinstance(value, dict):
        raise ValidationError('Social links must be an object.')
    allowed = {'website', 'linkedin', 'github', 'twitter', 'youtube', 'facebook', 'instagram'}
    invalid = set(value.keys()) - allowed
    if invalid:
        raise ValidationError(f'Unsupported social link keys: {", ".join(sorted(invalid))}.')


def validate_skill_list(value):
    if not isinstance(value, list):
        raise ValidationError('Skills must be a list.')
    if len(value) > 40:
        raise ValidationError('A user can list up to 40 skills.')
    for skill in value:
        if not isinstance(skill, str) or not re.match(r'^[\w\s+#.-]{2,60}$', skill):
            raise ValidationError('Each skill must be a readable text value between 2 and 60 characters.')
