class ValidationError(Exception):
    """Базовый класс исключений для валидаторов."""

class ShortError(ValidationError):
    """Исключение для валидатора короткого идентификатора."""