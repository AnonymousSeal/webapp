from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired
from datetime import datetime
from pytz import timezone


tz = timezone('Europe/Vienna')

class CommentForm(FlaskForm):
    content = TextAreaField('Content')
    submit = SubmitField('Comment')

class UploadForm(FlaskForm):
    upload = FileField('Upload', validators=[DataRequired(), FileAllowed(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'pptx', 'xlsx', 'gap'])])
    submit = SubmitField('Upload File')

class AddTaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    deadline_date = DateField('Deadline', validators=[DataRequired()], default=datetime.now(tz))
    deadline_time = TimeField('Deadline', validators=[DataRequired()], default=datetime.now(tz))
    subject = SelectField('Subject', choices=[], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add')
