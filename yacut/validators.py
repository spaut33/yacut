from wtforms.validators import ValidationError

from .models import URLMap

FORM_SHORT_ERROR_MESSAGE = 'Имя {name} уже занято!'


class ValidateShort:
    """Валидатор для проверки короткого идентификатора."""

    def __init__(self):
        pass

    def __call__(self, form, field):
        try:
            URLMap.validate_short(
                field.data,
                error_message=FORM_SHORT_ERROR_MESSAGE.format(name=field.data),
            )
        except ValueError as error:
            raise ValidationError(str(error))


class ValidateOriginal:
    """Валидатор для проверки оригинальной ссылки."""

    def __call__(self, form, field):
        try:
            URLMap.validate_original(field.data)
        except ValueError as error:
            raise ValidationError(str(error))
