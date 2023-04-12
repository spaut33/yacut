from flask import jsonify, request

from settings import Config
from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap

URL_NOT_FOUND = 'Указанный id не найден'
BODY_NOT_FOUND = 'Отсутствует тело запроса'
DATA_NOT_FOUND = '"url" является обязательным полем!'
TOO_LONG_ERROR_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
UNIQUE_SHORT_ERROR_MESSAGE = 'Имя "{name}" уже занято.'
NON_ALPHANUMERIC_ERROR_MESSAGE = 'Указано недопустимое имя для короткой ссылки'


def validate_alphanumeric(data):
    """Проверка данных на соответствие шаблону."""
    return Config.CUSTOM_ID_PATTERN.match(data) is not None


@app.route('/api/id/<short_link>/', methods=['GET'])
def get_url(short_link):
    """Получение ссылки по короткой ссылке"""
    url_map = URLMap.get_link_by_short(short_link)
    if url_map is None:
        raise InvalidAPIUsage(URL_NOT_FOUND, 404)
    return jsonify({'url': url_map.original}), 200


@app.route('/api/id/', methods=['POST'])
def create_url():
    """Создание короткой ссылки"""
    data = request.get_json()

    if data is None:
        raise InvalidAPIUsage(BODY_NOT_FOUND)
    if 'url' not in data:
        raise InvalidAPIUsage(DATA_NOT_FOUND)
    custom_id = data.get('custom_id')
    if custom_id and not URLMap.is_short_link_unique(custom_id):
        raise InvalidAPIUsage(
            UNIQUE_SHORT_ERROR_MESSAGE.format(name=custom_id)
        )
    if custom_id and len(custom_id) > Config.SHORT_LINK_LENGTH:
        raise InvalidAPIUsage(TOO_LONG_ERROR_MESSAGE)
    if custom_id and not validate_alphanumeric(custom_id):
        raise InvalidAPIUsage(NON_ALPHANUMERIC_ERROR_MESSAGE)
    if not URLMap.is_original_link_unique(data['url']):
        raise InvalidAPIUsage(Config.UNIQUE_ERROR_MESSAGE)

    url_map = URLMap.create(
        original=data['url'], short=custom_id or URLMap.generate_short_link()
    )
    return (
        jsonify(
            {'url': url_map.original, 'short_link': url_map.full_short_link()}
        ),
        201,
    )
