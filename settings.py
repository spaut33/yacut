import os
import re
from string import ascii_letters, digits


class Config:
    """Базовый класс для настроек приложения."""

    SECRET_KEY = os.getenv('SECRET_KEY', default='SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', default='sqlite:///db.sqlite3'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ORIGINAL_LINK_LENGTH = 2000  # Длина оригинальной ссылки
    SHORT_LINK_LENGTH = 16  # Длина короткой ссылки
    GENERATED_LINK_LENGTH = 6  # Длина короткой ссылки для генерации
    # Регулярное выражение для короткого имени
    ALLOWED_SYMBOLS = ascii_letters + digits
    CUSTOM_ID_PATTERN = re.compile(rf'^[{ALLOWED_SYMBOLS}]+$')
    REDIRECT_VIEW = 'redirect_view'  # Имя вьюхи для редиректа
    # Сообщение об ошибке для уникальности оригинальной ссылки
    UNIQUE_ERROR_MESSAGE = 'Такая ссылка уже есть в базе'


if __name__ == '__main__':
    assert Config.CUSTOM_ID_PATTERN.match('abc123') is not None
    assert Config.CUSTOM_ID_PATTERN.match('abc123!&^') is None
