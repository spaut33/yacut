from flask import render_template, flash, redirect, abort

from . import app
from .forms import URLMapForm
from .models import URLMap
from settings import Config


UNIQUE_SHORT_ERROR_MESSAGE = 'Имя {name} уже занято!'
ERROR_MESSAGE_STYLE = 'danger'
LINK_TYPE_ERROR_MESSAGE = 'Неверный тип ссылки: {link_type}'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Главная страница"""
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    if form.custom_id and not URLMap.is_short_link_unique(form.custom_id.data):
        flash(
            UNIQUE_SHORT_ERROR_MESSAGE.format(name=form.custom_id.data),
            ERROR_MESSAGE_STYLE,
        )
        return render_template('index.html', form=form)
    if not URLMap.is_original_link_unique(form.original_link.data):
        flash(Config.UNIQUE_ERROR_MESSAGE, ERROR_MESSAGE_STYLE)
        return render_template('index.html', form=form)

    url_map = URLMap.create(
        form.original_link.data,
        form.custom_id.data or URLMap.generate_short_link(),
    )
    return render_template(
        'index.html', form=form, full_link=url_map.full_short_link()
    )


@app.route('/<short_link>', methods=['GET'])
def redirect_view(short_link):
    """Перенаправление на оригинальную ссылку"""
    url_map = URLMap.get_link_by_short(short_link)
    if url_map is not None:
        return redirect(url_map.original)
    abort(404)
