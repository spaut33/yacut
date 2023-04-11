import re

from flask import jsonify, request

from settings import Config
from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import (
    UNIQUE_ERROR_MESSAGE,
    full_short_link,
    generate_short_link,
    is_link_unique,
)

URL_NOT_FOUND = 'Указанный id не найден'
BODY_NOT_FOUND = 'Отсутствует тело запроса'
DATA_NOT_FOUND = '"url" является обязательным полем!'
TOO_LONG_ERROR_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
UNIQUE_SHORT_ERROR_MESSAGE = 'Имя "{name}" уже занято.'
NON_ALPHANUMERIC_ERROR_MESSAGE = 'Указано недопустимое имя для короткой ссылки'


def validate_alphanumeric(data):
    """Проверка данных на соответствие шаблону."""
    pattern = re.compile(Config.CUSTOM_ID_PATTERN)
    return pattern.match(data) is not None


@app.route('/api/id/<short_link>/', methods=['GET'])
def get_url(short_link):
    """Получение ссылки по короткой ссылке"""
    url_map = URLMap.query.filter_by(short=short_link).first()
    if url_map is None:
        raise InvalidAPIUsage(URL_NOT_FOUND, 404)
    return jsonify({'url': url_map.to_dict()['url']}), 200


@app.route('/api/id/', methods=['POST'])
def create_url():
    """Создание короткой ссылки"""
    data = request.get_json()

    if data is None:
        raise InvalidAPIUsage(BODY_NOT_FOUND)
    if 'url' not in data:
        raise InvalidAPIUsage(DATA_NOT_FOUND)
    custom_id = data.get('custom_id')
    if custom_id and not is_link_unique(custom_id, 'short'):
        raise InvalidAPIUsage(
            UNIQUE_SHORT_ERROR_MESSAGE.format(name=custom_id)
        )
    if custom_id and len(custom_id) > Config.SHORT_LINK_LENGTH:
        raise InvalidAPIUsage(TOO_LONG_ERROR_MESSAGE)
    if custom_id and not validate_alphanumeric(custom_id):
        raise InvalidAPIUsage(NON_ALPHANUMERIC_ERROR_MESSAGE)
    if not is_link_unique(data['url'], 'original'):
        raise InvalidAPIUsage(UNIQUE_ERROR_MESSAGE)

    url_map = URLMap(
        original=data['url'], short=custom_id or generate_short_link()
    )
    db.session.add(url_map)
    db.session.commit()
    return (
        jsonify(
            {
                'url': url_map.to_dict()['url'],
                'short_link': full_short_link(url_map.to_dict()['short_link']),
            }
        ),
        201,
    )
