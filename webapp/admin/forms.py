from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class DeleteAllForm(FlaskForm):
    table = StringField('Таблица', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Удалить всё', render_kw={"class": "btn btn-primary"})
