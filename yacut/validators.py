from wtforms.validators import ValidationError

from .exceptions import ShortError
from .models import URLMap

FORM_SHORT_ERROR_MESSAGE = 'Имя {name} уже занято!'


class ValidateShort:
    """Валидатор для проверки короткого идентификатора."""

    def __call__(self, form, field):
        try:
            URLMap.validate_short(field.data)
        except ValueError as error:
            raise ValidationError(str(error))
        except ShortError:
            raise ValidationError(
                FORM_SHORT_ERROR_MESSAGE.format(name=field.data)
            )


class ValidateOriginal:
    """Валидатор для проверки оригинальной ссылки."""

    def __call__(self, form, field):
        try:
            URLMap.validate_original(field.data)
        except ValueError as error:
            raise ValidationError(str(error))
