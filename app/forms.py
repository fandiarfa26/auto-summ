from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired 

class SentenceForm(FlaskForm):
    sentence1 = StringField('Sentences', widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('Process')

class BookUploadForm(FlaskForm):
    title = StringField('Book Title', validators=[DataRequired()])
    file = FileField('File PDF', validators=[FileRequired()])