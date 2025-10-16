from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, MultipleFileField
from wtforms import SubmitField


class FileForm(FlaskForm):
    files = MultipleFileField('Upload a file',
                     validators=[
                         FileRequired(message='No file was selected.'),
                     ])
    submit = SubmitField("Upload your file/s")