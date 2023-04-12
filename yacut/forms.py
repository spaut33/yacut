from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from settings import Config

URL_FIELD_TEXT = 'Введите URL'
CUSTOM_ID_TEXT = 'Введите короткое имя'
SUBMIT_TEXT = 'Создать'
FIELD_REQUIRED = 'Обязательное поле'
URL_LENGTH_MESSAGE = (
    f'URL должен быть длиной от 1 до {Config.ORIGINAL_LINK_LENGTH} символов'
)
CUSTOM_ID_LENGTH_MESSAGE = (
    f'Короткое имя должно быть длиной от 1 до '
    'Config.USER_SHORT_LENGTH} символов'
)
CUSTOM_ID_REGEXP_MESSAGE = (
    'Короткое имя должно состоять только из латинских букв и цифр'
)


class URLMapForm(FlaskForm):
    """Форма для сокращения URL."""

    original_link = URLField(
        URL_FIELD_TEXT,
        validators=[
            DataRequired(message=FIELD_REQUIRED),
            Length(
                max=Config.ORIGINAL_LINK_LENGTH, message=URL_LENGTH_MESSAGE
            ),
        ],
    )
    custom_id = StringField(
        CUSTOM_ID_TEXT,
        validators=[
            Optional(),
            Length(
                max=Config.USER_SHORT_LENGTH, message=CUSTOM_ID_LENGTH_MESSAGE
            ),
            Regexp(Config.SHORT_PATTERN, message=CUSTOM_ID_REGEXP_MESSAGE),
        ],
    )
    submit = SubmitField(SUBMIT_TEXT)
