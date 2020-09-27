from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, FormField
from wtforms.validators import DataRequired, ValidationError

class CommentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content')

class UploadForm(FlaskForm):
    upload = FileField('Upload', validators=[DataRequired()])

    # def validate_extension(self, upload):
    #     if not '.' in upload.data or not upload.data.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']:
    #         raise ValidationError('This file extension is not allowed')

class CommentUploadForm(FlaskForm):
    comment = FormField(CommentForm)
    upload = FormField(UploadForm)
    vars = []
