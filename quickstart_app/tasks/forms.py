from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, FormField
from wtforms.validators import DataRequired, ValidationError

class CommentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content')

class UploadForm(FlaskForm):
    upload = FileField('Upload', validators=[DataRequired(), FileAllowed(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'pptx', 'xlsx'])])

class CommentUploadForm(FlaskForm):
    comment = FormField(CommentForm)
    upload = FormField(UploadForm)
