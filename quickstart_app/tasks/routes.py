from flask_login import current_user, login_required
from flask import render_template, request, redirect, url_for, send_from_directory, abort, current_app, Blueprint, session, flash
from quickstart_app.models import Task, Subject, Material, Comment
from quickstart_app.tasks.forms import CommentUploadForm, AddTaskForm
from quickstart_app.tasks.utils import check_comment_cu_session_data, add_file
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
    check_comment_cu_session_data(task_id)

    task = Task.query.get_or_404(task_id)

    if "add" in request.form and form.upload.validate(form):
        add_file(form.upload.upload.data, secure_filename(task.name))

    if "comment" in request.form and form.comment.validate(form):
        # add comment
        comment = Comment(comment=form.comment.content.data, author_id=current_user.id, task_id=task_id)
        db.session.add(comment)
        db.session.commit()
        # add associated material
        for filename, orignial_name in session['file_chache']:
            db.session.add(Material(filename=filename, orignial_name=orignial_name, upload_id=comment.id))
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
    check_comment_cu_session_data(str(comment.task_id) + 'u' + str(comment.id), initial_file_cache_value=[[material.filename, material.orignial_name] for material in comment.material])

    if "add" in request.form and form.upload.validate(form):
        add_file(form.upload.upload.data, secure_filename(comment.task.name))

    if "comment" in request.form and form.comment.validate(form):
        comment.comment = form.comment.content.data
        #rm removed material
        for material in comment.material:
            if [material.filename, material.orignial_name] not in session['file_chache']:
                 db.session.delete(material)
        #add added material
        material_filenames = [material.filename for material in comment.material]
        for filename, orignial_name in session['file_chache']:
            if filename not in material_filenames:
                 db.session.add(Material(filename=filename, orignial_name=orignial_name, upload_id=comment.id))
        db.session.commit()
        return redirect(url_for('tasks.task', task_id=comment.task_id))

    if request.method == 'GET':
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
        try:
            os.remove(os.path.join(current_app.root_path, 'static/material', material.filename))
        except:
            pass
    db.session.commit()
    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been deleted!', 'success')
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
