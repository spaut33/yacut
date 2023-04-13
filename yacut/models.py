from datetime import datetime as dt
from random import choices

from flask import url_for

from settings import Config
from yacut import db

from .exceptions import ShortError

SHORT_ERROR_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
URL_ERROR_MESSAGE = 'Введен неправильный URL'
SHORT_GENERATION_ERROR = (
    'Не удалось сгенерировать короткую ссылку за '
    f'{Config.GENERATE_SHORT_RETRIES} попыток'
)


class URLMap(db.Model):
    """Модель для хранения отображений URL-адресов."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(
        db.String(Config.ORIGINAL_LINK_LENGTH), unique=False, nullable=False
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
        for _ in range(Config.GENERATE_SHORT_RETRIES):
            short_link = ''.join(
                choices(Config.ALLOWED_SYMBOLS, k=Config.SHORT_LENGTH)
            )
            if URLMap.get_urlmap_by_short(short_link) is None:
                return short_link
        raise ValueError(SHORT_GENERATION_ERROR)

    def short_link(self):
        """Возвращает полную сокращенную ссылку, включая схему и хост"""
        return url_for(Config.REDIRECT_VIEW, short=self.short, _external=True)

    @staticmethod
    def validate_short(short):
        """Проверяет короткую ссылку на соответствие требованиям"""
        if len(short) > Config.USER_SHORT_LENGTH:
            raise ValueError(SHORT_ERROR_MESSAGE)
        if Config.SHORT_PATTERN.match(short) is None:
            raise ValueError(SHORT_ERROR_MESSAGE)
        if URLMap.get_urlmap_by_short(short) is not None:
            raise ShortError()

    @staticmethod
    def validate_original(original):
        """Проверяет оригинальную ссылку на соответствие требованиям"""
        if len(original) > Config.ORIGINAL_LINK_LENGTH:
            raise ValueError(URL_ERROR_MESSAGE)

    @staticmethod
    def create(original, short, validate=False):
        """Создает новую запись в БД"""
        if validate:
            URLMap.validate_original(original)
        if not short:
            short = URLMap.generate_short()
        elif validate:
            URLMap.validate_short(short)
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map
