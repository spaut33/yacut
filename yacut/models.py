from datetime import datetime as dt
from random import choices

from flask import url_for

from settings import Config
from yacut import db


class URLMap(db.Model):
    """Модель для хранения отображений URL-адресов."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(
        db.String(Config.ORIGINAL_LINK_LENGTH), unique=True, nullable=False
    )
    short = db.Column(
        db.String(Config.SHORT_LINK_LENGTH), unique=True, nullable=False
    )
    timestamp = db.Column(db.DateTime, index=True, default=dt.utcnow)

    def to_dict(self):
        """Возвращает словарь с данными модели."""
        return dict(url=self.original, short_link=self.short)

    @staticmethod
    def is_original_link_unique(link):
        """Проверяет уникальность оригинальной ссылки"""
        return URLMap.query.filter_by(original=link).first() is None

    @staticmethod
    def is_short_link_unique(link):
        """Проверяет уникальность короткой ссылки"""
        return URLMap.query.filter_by(short=link).first() is None

    @staticmethod
    def _generate_random_short_link():
        """Генерирует случайную короткую ссылку"""
        return ''.join(
            choices(Config.ALLOWED_SYMBOLS, k=Config.GENERATED_LINK_LENGTH)
        )

    @staticmethod
    def get_link_by_short(short_link):
        """Возвращает запись из БД по короткой ссылке"""
        return URLMap.query.filter_by(short=short_link).first()

    @staticmethod
    def generate_short_link():
        """Генерирует уникальную короткую ссылку"""
        while True:
            short_link = URLMap._generate_random_short_link()
            if URLMap.is_short_link_unique(short_link):
                break
        return short_link

    def full_short_link(self):
        """Возвращает полную сокращенную ссылку, включая схему и хост"""
        return url_for(
            Config.REDIRECT_VIEW, short_link=self.short, _external=True
        )

    @staticmethod
    def create(original, short=None):
        """Создает новую запись в БД"""
        url_map = URLMap(
            original=original, short=short or URLMap.generate_short_link()
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map
