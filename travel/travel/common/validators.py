from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


def validate_only_letters(value):
    for ch in value:
        if not ch.isalnum():
            raise ValidationError('This field must contain only letters')


def validate_name_chars(value):
    for ch in value:
        if not ch.isalnum() and not ch == ' ':
            raise ValidationError('This field must contain only letters, numbers or spaces')


@deconstructible
class MinDateValidator:
    def __init__(self, min_date):
        self.min_date = min_date

    def __call__(self, value):
        if value < self.min_date:
            raise ValidationError(f'Date must be greater than {self.min_date}')


@deconstructible
class MaxDateValidator:
    def __init__(self, max_date):
        self.max_date = max_date

    def __call__(self, value):
        if self.max_date < value:
            raise ValidationError(f'Date must be earlier than {self.max_date}')
