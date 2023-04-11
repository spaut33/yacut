from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional

from settings import Config


class URLMapForm(FlaskForm):
    """Форма для сокращения URL."""

    original_link = URLField(
        'Введите URL',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(
                min=1,
                max=Config.ORIGINAL_LINK_LENGTH,
                message=f'URL должен быть длиной от 1 до '
                f'{Config.ORIGINAL_LINK_LENGTH} символов',
            ),
        ],
    )
    short_link = StringField(
        'Введите короткое имя',
        validators=[
            Optional(),
            Length(
                1,
                max=Config.SHORT_LINK_LENGTH,
                message=f'Короткое имя должно быть длиной от 1 до '
                f'{Config.SHORT_LINK_LENGTH} символов',
            ),
        ],
    )
    submit = SubmitField('Создать')
