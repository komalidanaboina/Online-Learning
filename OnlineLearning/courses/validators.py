from django.core.exceptions import ValidationError


def validate_discount_price(course):
    if course.discount_price is not None and course.discount_price > course.price:
        raise ValidationError({'discount_price': 'Discount price cannot be greater than regular price.'})


def validate_json_string_list(value):
    if not isinstance(value, list):
        raise ValidationError('Expected a list.')
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValidationError('Each item must be non-empty text.')
