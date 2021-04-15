from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    author = StringField('Автор', validators=[DataRequired()])
    genre = StringField('Жанр', validators=[DataRequired()])
    created_date = IntegerField('Год создания', validators=[DataRequired()])
    annotation = TextAreaField('Аннотация', validators=[DataRequired()])
    img_file = FileField('Обложка', validators=[DataRequired()])
    text_file = FileField('PDF файд', validators=[DataRequired()])
    submit = SubmitField('Применить')
