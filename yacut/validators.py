from wtforms.validators import ValidationError

from .models import URLMap


class ValidateShort:
    """Валидатор для проверки короткого идентификатора."""
    def __init__(self, is_api=False):
        self.is_api = is_api

    def __call__(self, form, field):
        try:
            URLMap.validate_short(field.data, is_api=self.is_api)
        except ValueError as error:
            raise ValidationError(str(error))


class ValidateOriginal:
    """Валидатор для проверки оригинальной ссылки."""
    def __call__(self, form, field):
        try:
            URLMap.validate_original(field.data)
        except ValueError as error:
            raise ValidationError(str(error))
