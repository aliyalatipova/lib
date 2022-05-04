from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    # is_private = BooleanField("Личное")
    price = IntegerField("Цена")
    city = StringField('Город')
    img_href = StringField('Изображение')
    submit = SubmitField('Применить')
