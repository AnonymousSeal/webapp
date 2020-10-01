from flask_login import current_user, login_required
from flask import render_template, request, redirect, url_for, send_from_directory, abort, current_app, Blueprint, session, flash
from quickstart_app.models import Task, Subject, Material, Comment
from quickstart_app.tasks.forms import CommentUploadForm, AddTaskForm
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

@tasks.route('/comment/<int:task_id>', methods=['GET', 'POST'])
@login_required
def add_comment(task_id):
    form = CommentUploadForm()
    if not 'file_chache' in session:
        session['file_chache'] = []
    if not 'staged_files_location' in session:
        session['staged_files_location'] = task_id
    if session['staged_files_location'] != task_id:
        session['file_chache'] = []
        session['staged_files_location'] = task_id

    if "add" in request.form and form.upload.validate(form):
        filename = secure_filename(form.upload.upload.data.filename)
        form.upload.upload.data.save(os.path.join(current_app.root_path, 'static/material', filename))
        if session['file_chache'] != []:
            session['file_chache'] = session['file_chache'] + [filename]
        else:
            session['file_chache'] = [filename]

    if "comment" in request.form and form.comment.validate(form):
        comment = Comment(title=form.comment.title.data, comment=form.comment.content.data, author_id=current_user.id, task_id=task_id)
        db.session.add(comment)
        db.session.commit()
        for filename in session['file_chache']:
            db.session.add(Material(filename=filename, upload_id=comment.id))
        db.session.commit()
        session['file_chache'] = []

        return redirect(url_for('tasks.task', task_id=task_id))
    return render_template('comment.html', title='Add Comment',
                            form=form, legend='Add Comment')

@tasks.route('/comment/<int:comment_id>/update', methods=['GET', 'POST'])
@login_required
def update_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user:
        abort(403)
    form = CommentUploadForm()

    if not 'file_chache' in session:
        session['file_chache'] = [material.filename for material in comment.material]
    if not 'staged_files_location' in session:
        session['staged_files_location'] = str(comment.task_id) + 'u' + str(comment.id)
    if session['staged_files_location'] != str(comment.task_id) + 'u' + str(comment.id):
        session['file_chache'] = [material.filename for material in comment.material]
        session['staged_files_location'] = str(comment.task_id) + 'u' + str(comment.id)

    if "add" in request.form and form.upload.validate(form):
        filename = secure_filename(form.upload.upload.data.filename)
        form.upload.upload.data.save(os.path.join(current_app.root_path, 'static/material', filename))
        if session['file_chache'] != []:
            session['file_chache'] = session['file_chache'] + [filename]
        else:
            session['file_chache'] = [filename]

    if "comment" in request.form and form.comment.validate(form):
        comment.title = form.comment.title.data
        comment.comment = form.comment.content.data
        for material in comment.material:
            if material.filename not in session['file_chache']:
                 db.session.delete(material)
        material_filenames = [material.filename for material in comment.material]
        for filename in session['file_chache']:
            if filename not in material_filenames:
                 db.session.add(Material(filename=filename, upload_id=comment.id))
        db.session.commit()
        return redirect(url_for('tasks.task', task_id=comment.task_id))

    if request.method == 'GET':
        form.comment.title.data = comment.title
        form.comment.content.data = comment.comment

    return render_template('comment.html', title='Update Comment',
                            form=form, legend='Update Comment')

@tasks.route('/comment/<int:comment_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user:
        abort(403)
    for material in comment.material:
        db.session.delete(material)
    db.session.commit()
    db.session.delete(comment)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('tasks.task', task_id=comment.task_id))

@tasks.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    if current_user.status == 'user':
        return redirect(url_for('users.profile', username=current_user.username))

    form = AddTaskForm()
    form.subject.choices = [(subject.id, subject.name) for subject in Subject.query.all()]

    if form.validate_on_submit():
        db.session.add(Task(name=form.title.data,
                            description=form.description.data,
                            deadline=datetime.combine(form.deadline_date.data,
                            form.deadline_time.data),
                            user_id=current_user.id,
                            subject_id=form.subject.data))
        db.session.commit()
        flash('Task has been added.', 'success')
        return redirect(url_for('tasks.schedule'))
    return render_template('add_task.html', title='Add Task', form=form)

@tasks.route('/uploads/<string:filename>')
@login_required
def uploaded_file(filename):
    try:
        return send_from_directory(os.path.join(current_app.root_path, 'static/material'), filename=filename, as_attachment=False)
    except FileNotFoundError:
        abort(404)
