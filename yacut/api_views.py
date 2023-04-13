from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap

URL_NOT_FOUND = 'Указанный id не найден'
BODY_NOT_FOUND = 'Отсутствует тело запроса'
DATA_NOT_FOUND = '"url" является обязательным полем!'
API_SHORT_ERROR_MESSAGE = 'Имя "{name}" уже занято.'


@app.route('/api/id/<short_link>/', methods=['GET'])
def get_url(short_link):
    """Получение ссылки по короткой ссылке"""
    url_map = URLMap.get_urlmap_by_short(short_link)
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
    short = data.get('custom_id')
    try:
        url_map = URLMap.create(
            original=data['url'],
            short=short,
            validate=True,
            error_message=API_SHORT_ERROR_MESSAGE.format(name=short),
        )
        return (
            jsonify(
                {'url': url_map.original, 'short_link': url_map.short_link()}
            ),
            201,
        )
    except ValueError as error:
        raise InvalidAPIUsage(str(error))
