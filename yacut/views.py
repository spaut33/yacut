from flask import render_template, flash, redirect, abort

from . import app
from .forms import URLMapForm
from .models import URLMap

ERROR_MESSAGE_STYLE = 'danger'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Главная страница"""
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        url_map = URLMap.create(
            form.original_link.data,
            form.custom_id.data,
        )
        return render_template(
            'index.html', form=form, full_link=url_map.short_link()
        )
    except ValueError as error:
        flash(str(error), ERROR_MESSAGE_STYLE)
        return render_template('index.html', form=form)


@app.route('/<short>', methods=['GET'])
def redirect_view(short):
    """Перенаправление на оригинальную ссылку"""
    url_map = URLMap.get_urlmap_by_short(short)
    if url_map is not None:
        return redirect(url_map.original)
    abort(404)
