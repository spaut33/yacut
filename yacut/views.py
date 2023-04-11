import secrets
import string

from flask import render_template, flash, url_for, redirect, abort
from markupsafe import Markup

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from settings import Config


SUCCESS_MESSAGE = 'Ваша ссылка укорочена: {url}'
UNIQUE_ERROR_MESSAGE = 'Такая ссылка уже есть в базе'
UNIQUE_SHORT_ERROR_MESSAGE = 'Имя {name} уже занято!'
SUCCESS_MESSAGE_STYLE = 'primary'
ERROR_MESSAGE_STYLE = 'danger'
LINK_TYPE_ERROR_MESSAGE = 'Неверный тип ссылки: {link_type}'


def generate_short_link():
    """Генерирует короткую ссылку"""
    return ''.join(
        secrets.choice(string.ascii_letters + string.digits)
        for _ in range(Config.GENERATED_LINK_LENGTH)
    )


def full_short_link(short_link):
    """Возвращает полную короткую ссылку"""
    return url_for('redirect_view', short_link=short_link, _external=True)


def is_link_unique(link, link_type):
    """Проверяет уникальность ссылки"""
    if link_type == 'original':
        return URLMap.query.filter_by(original=link).first() is None
    elif link_type == 'short':
        return URLMap.query.filter_by(short=link).first() is None
    else:
        raise ValueError(LINK_TYPE_ERROR_MESSAGE.format(link_type=link_type))


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Главная страница"""
    form = URLMapForm()
    if form.validate_on_submit():
        if form.custom_id and not is_link_unique(form.custom_id.data, 'short'):
            flash(
                UNIQUE_SHORT_ERROR_MESSAGE.format(name=form.custom_id.data),
                ERROR_MESSAGE_STYLE,
            )
            return render_template('index.html', form=form)
        if not is_link_unique(form.original_link.data, 'original'):
            flash(UNIQUE_ERROR_MESSAGE, ERROR_MESSAGE_STYLE)
            return render_template('index.html', form=form)

        short_link = form.custom_id.data or generate_short_link()
        url_map = URLMap(original=form.original_link.data, short=short_link)
        db.session.add(url_map)
        db.session.commit()
        full_link = full_short_link(short_link)
        flash(
            Markup(
                SUCCESS_MESSAGE.format(
                    url=f'<a href="{full_link}">{full_link}</a>'
                )
            ),
            SUCCESS_MESSAGE_STYLE,
        )
    return render_template('index.html', form=form)


@app.route('/<short_link>', methods=['GET'])
def redirect_view(short_link):
    """Перенаправление на оригинальную ссылку"""
    url_map = URLMap.query.filter_by(short=short_link).first()
    if url_map is not None:
        return redirect(url_map.original)
    abort(404)
