from datetime import datetime as dt

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
        return dict(
            url=self.original,
            short_link=self.short,
        )

    def from_dict(self, data, field='url'):
        """Заполняет модель данными из словаря."""
        if field in data:
            setattr(self, field, data[field])
