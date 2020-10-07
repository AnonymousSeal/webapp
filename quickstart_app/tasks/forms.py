from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
from wtforms.fields.html5 import DateField, TimeField
from quickstart_app.models import Subject
from datetime import datetime

class CommentForm(FlaskForm):
    content = TextAreaField('Content')
    submit = SubmitField('Comment')

class UploadForm(FlaskForm):
    upload = FileField('Upload', validators=[DataRequired(), FileAllowed(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'pptx', 'xlsx'])])
    submit = SubmitField('Upload File')

class AddTaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    deadline_date = DateField('Deadline', validators=[DataRequired()], default=datetime.utcnow())
    deadline_time = TimeField('Deadline', validators=[DataRequired()], default=datetime.utcnow())
    subject = SelectField('Subject', choices=[], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add')
