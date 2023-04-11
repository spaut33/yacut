from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import (
    UNIQUE_ERROR_MESSAGE,
    UNIQUE_SHORT_ERROR_MESSAGE,
    full_short_link,
    generate_short_link,
    is_link_unique,
)

URL_NOT_FOUND = 'Ссылка не найдена'
DATA_NOT_FOUND = 'В запросе отсутствуют обязательные поля'


@app.route('/api/id/<short_link>', methods=['GET'])
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
    custom_id = data.get('custom_id')

    if data is None or 'url' not in data:
        raise InvalidAPIUsage(DATA_NOT_FOUND)
    if not is_link_unique(data['url'], 'original'):
        raise InvalidAPIUsage(UNIQUE_ERROR_MESSAGE)
    if custom_id and not is_link_unique(custom_id, 'short'):
        raise InvalidAPIUsage(UNIQUE_SHORT_ERROR_MESSAGE)
    url_map = URLMap(
        original=data['url'], short=custom_id or generate_short_link()
    )
    db.session.add(url_map)
    db.session.commit()
    return jsonify({'url': full_short_link(url_map.to_dict()['short'])}), 201
