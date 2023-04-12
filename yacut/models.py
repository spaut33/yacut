from datetime import datetime as dt
from random import choices

from flask import url_for

from settings import Config
from yacut import db

SHORT_ERROR_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
FORM_SHORT_ERROR_MESSAGE = 'Имя {name} уже занято!'
UNIQUE_ERROR_MESSAGE = 'Такая ссылка уже есть в базе'
URL_ERROR_MESSAGE = 'Введен неправильный URL'
API_SHORT_ERROR_MESSAGE = 'Имя "{name}" уже занято.'


def validate_alphanumeric(data):
    """Проверка данных на соответствие шаблону."""
    return Config.SHORT_PATTERN.match(data) is not None


class URLMap(db.Model):
    """Модель для хранения отображений URL-адресов."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(
        db.String(Config.ORIGINAL_LINK_LENGTH), unique=True, nullable=False
    )
    short = db.Column(
        db.String(Config.USER_SHORT_LENGTH), unique=True, nullable=False
    )
    timestamp = db.Column(db.DateTime, index=True, default=dt.utcnow)

    @staticmethod
    def get_urlmap_by_original(original):
        """Получает запись из БД по оригинальной ссылке"""
        return URLMap.query.filter_by(original=original).first()

    @staticmethod
    def get_urlmap_by_short(short):
        """Возвращает запись из БД по короткой ссылке"""
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def generate_short():
        """Генерирует уникальный короткий идентификатор"""
        while True:
            short_link = ''.join(
                choices(Config.ALLOWED_SYMBOLS, k=Config.SHORT_LENGTH)
            )
            if URLMap.get_urlmap_by_short(short_link) is None:
                break
        return short_link

    def short_link(self):
        """Возвращает полную сокращенную ссылку, включая схему и хост"""
        return url_for(Config.REDIRECT_VIEW, short=self.short, _external=True)

    @staticmethod
    def validate_short(short, is_api=False):
        """Проверяет короткую ссылку на соответствие требованиям"""
        if len(short) > Config.USER_SHORT_LENGTH:
            raise ValueError(SHORT_ERROR_MESSAGE)
        if not validate_alphanumeric(short):
            raise ValueError(SHORT_ERROR_MESSAGE)
        if URLMap.get_urlmap_by_short(short) is not None:
            if is_api:
                raise ValueError(API_SHORT_ERROR_MESSAGE.format(name=short))
            raise ValueError(FORM_SHORT_ERROR_MESSAGE.format(name=short))

    @staticmethod
    def validate_original(original):
        """Проверяет оригинальную ссылку на соответствие требованиям"""
        if len(original) > Config.ORIGINAL_LINK_LENGTH:
            raise ValueError(URL_ERROR_MESSAGE)
        if URLMap.get_urlmap_by_original(original) is not None:
            raise ValueError(UNIQUE_ERROR_MESSAGE.format(name=original))

    @staticmethod
    def create(original, short=None, is_api=False):
        """Создает новую запись в БД"""
        if short:
            URLMap.validate_short(short, is_api=is_api)
        URLMap.validate_original(original)
        url_map = URLMap(
            original=original, short=short or URLMap.generate_short()
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map
