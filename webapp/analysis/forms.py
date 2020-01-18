from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class QueryForm(FlaskForm):
    query = StringField('Строка запроса', validators=[DataRequired()], render_kw={"class": "form-control"})
    category = SelectField('Категория', validators=[DataRequired()], coerce=int, render_kw={"class": "form-control"})
    age = SelectField('Глубина', validators=[DataRequired()], coerce=int, render_kw={"class": "form-control"})
    submit = SubmitField('Отправить!', render_kw={"class": "btn btn-primary"})
