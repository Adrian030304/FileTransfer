from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, MultipleFileField
from wtforms import SubmitField, SelectField


class FileForm(FlaskForm):
    files = MultipleFileField('Upload a file',
                     validators=[
                         FileRequired(message='No file was selected.'),
                     ])
    expiration_date = SelectField("Expiration Time", choices=[
        '2 minutes', '15 minutes', '30 minutes', '1 hour'
    ])
    submit = SubmitField("Upload your file/s")