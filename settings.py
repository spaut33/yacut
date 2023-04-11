import os


class Config:
    """Базовый класс для настроек приложения."""

    SECRET_KEY = os.getenv('SECRET_KEY', default='SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', default='sqlite:///db.sqlite3'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ORIGINAL_LINK_LENGTH = 256  # Длина оригинальной ссылки
    SHORT_LINK_LENGTH = 16  # Длина короткой ссылки
    GENERATED_LINK_LENGTH = 6  # Длина короткой ссылки для генерации
