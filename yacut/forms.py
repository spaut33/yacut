from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from settings import Config

URL_FIELD_TEXT = 'Введите URL'
CUSTOM_ID_TEXT = 'Введите короткое имя'
SUBMIT_TEXT = 'Создать'
FIELD_REQUIRED = 'Обязательное поле'
URL_LENGTH_MESSAGE = 'URL должен быть длиной от 1 до {length} символов'
CUSTOM_ID_LENGTH_MESSAGE = (
    'Короткое имя должно быть длиной от 1 до {length} символов'
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
                max=Config.ORIGINAL_LINK_LENGTH,
                message=URL_LENGTH_MESSAGE.format(
                    length=Config.ORIGINAL_LINK_LENGTH
                ),
            ),
        ],
    )
    custom_id = StringField(
        CUSTOM_ID_TEXT,
        validators=[
            Optional(),
            Length(
                max=Config.SHORT_LINK_LENGTH,
                message=CUSTOM_ID_LENGTH_MESSAGE.format(
                    length=Config.SHORT_LINK_LENGTH
                ),
            ),
            Regexp(Config.CUSTOM_ID_PATTERN, message=CUSTOM_ID_REGEXP_MESSAGE),
        ],
    )
    submit = SubmitField(SUBMIT_TEXT)
