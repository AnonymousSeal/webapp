from flask_login import current_user, login_required
from flask import render_template, request, redirect, url_for, send_from_directory, abort, current_app, Blueprint
from quickstart_app.models import Task, Subject, Material, Comment
from quickstart_app.tasks.forms import CommentUploadForm
from quickstart_app import db
from werkzeug.utils import secure_filename
from datetime import datetime
import os

tasks = Blueprint('tasks', __name__)

@tasks.route('/')
@tasks.route('/home')
@tasks.route('/schedule')
@login_required
def schedule():
    return render_template('schedule.html', title='Schedule', schedule=Task.query.all())

@tasks.route('/task/<int:task_id>')
@login_required
def task(task_id):
    task = Task.query.get(task_id)
    subject = Subject.query.get(task.subject_id)
    return render_template('task.html', title=task.name, task=task, subject=subject)

@tasks.route('/add_comment/<int:task_id>', methods=['GET', 'POST'])
@login_required
def add_comment(task_id):
    form = CommentUploadForm()

    if "add" in request.form and form.upload.validate(form):
        filename = secure_filename(form.upload.upload.data.filename)
        form.upload.upload.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        form.vars.append(form.upload.upload.data.filename)

    if "comment" in request.form and form.comment.validate(form):
        comment = Comment(title=form.comment.title.data, comment=form.comment.content.data, author_id=current_user.id, task_id=task_id)
        db.session.add(comment)
        db.session.commit()
        for var in form.vars:
            material = Material(filename=var, upload_id=comment.id)
            db.session.add(material)
        db.session.commit()
        form.vars = []

        return redirect(url_for('tasks.task', task_id=task_id))
    return render_template('add_comment.html', title='Add Comment', form=form)

@tasks.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    if current_user.status == 'user':
        return redirect(url_for('users.profile', username=current_user.username))
    if request.method == 'POST':
        db.session.add(Task(name=request.form['name'],
                            description=request.form['description'],
                            deadline=datetime.strptime(request.form['deadline_date'] + \
                            request.form['deadline_time'], '%Y-%m-%d%H:%M'),
                            user_id=current_user.id,
                            subject_id=request.form['subject']))
        db.session.commit()

        return redirect(url_for('tasks.schedule'))
    return render_template('add_task.html', title='Add Task', subjects=Subject.query.all())

@tasks.route('/uploads/<string:filename>')
@login_required
def uploaded_file(filename):
    try:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename=filename, as_attachment=False)
    except FileNotFoundError:
        abort(404)
