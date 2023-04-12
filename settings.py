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

    USER_SHORT_LENGTH = 16  # Длина короткой ссылки
    SHORT_LENGTH = 6  # Длина короткой ссылки для генерации
    GENERATE_SHORT_RETRIES = 10  # Количество попыток генерации короткой ссылки
    ALLOWED_SYMBOLS = re.escape(ascii_letters + digits)
    SHORT_PATTERN = re.compile(rf'^[{ALLOWED_SYMBOLS}]+$')

    REDIRECT_VIEW = 'redirect_view'  # Имя вьюхи для редиректа
