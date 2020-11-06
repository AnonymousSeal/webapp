from webapp import db
from webapp.main.utils import delete_file
from webapp.models import Comment, Material, Subject, Task
from webapp.tasks.forms import AddTaskForm, CommentForm, UploadForm
from webapp.tasks.utils import add_file
from flask import abort, Blueprint, current_app, flash, redirect, render_template, request, send_from_directory, url_for
from flask_login import current_user, login_required
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


@tasks.route('/comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def comment(comment_id):
    form = CommentForm()
    comment = Comment.query.get(comment_id)
    task = Task.query.get(comment.task_id)

    if form.validate_on_submit():
        comment.comment = form.content.data
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('tasks.task', task_id=task.id))

    if request.method == 'GET':
        form.content.data = comment.comment

    return render_template('comment.html', title=task.name, comment=comment, task=task, form=form)


@tasks.route('/task/<int:task_id>/comment', methods=['GET', 'POST'])
@login_required
def add_comment_content(task_id):
    form = CommentForm()

    task = Task.query.get_or_404(task_id)

    if form.validate_on_submit():
        # add comment
        comment = Comment(comment=form.content.data, author_id=current_user.id, task_id=task_id)
        db.session.add(comment)
        db.session.commit()

        return redirect(url_for('tasks.task', task_id=task_id))
    return render_template('comment_content.html', title='Add Comment',
                            form=form, task=task)


@tasks.route('/comment/<int:comment_id>/upload', methods=['GET', 'POST'])
@login_required
def add_comment_upload(comment_id):
    form = UploadForm()
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user:
        abort(403)

    if request.method == 'POST' and 'File' in request.form and form.validate():
        filename = add_file(form.upload.data, secure_filename(comment.task.name))
        db.session.add(Material(filename=filename, orignial_name=form.upload.data.filename, upload_id=comment.id))
        db.session.commit()
        return redirect(url_for('tasks.add_comment_upload', comment_id=comment_id))
    elif request.method == 'POST' and 'Photo' in request.form:
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        filename = add_file(file, secure_filename(comment.task.name))
        db.session.add(Material(filename=filename, orignial_name=file.filename, upload_id=comment.id))
        db.session.commit()
        return redirect(url_for('tasks.add_comment_upload', comment_id=comment_id))

    return render_template('comment_upload.html', title='Add Upload',
                            form=form, comment=comment)


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
    flash('Your comment has been deleted!', 'success')
    return redirect(url_for('tasks.task', task_id=comment.task_id))


@tasks.route('/upload/<int:upload_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_upload(upload_id):
    material = Material.query.get_or_404(upload_id)
    delete_file(material.filename, 'static/material', 'material')
    db.session.delete(material)
    db.session.commit()
    next_page = request.args.get('origin')
    if next_page:
        return redirect(next_page)
    return redirect(url_for('tasks.schedule'))


@tasks.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
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


@tasks.route('/task/<int:task_id>/update', methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if current_user.id != task.user_id and current_user.status == 'user':
        abort(403)

    form = AddTaskForm()
    form.subject.choices = [(subject.id, subject.name) for subject in Subject.query.all()]

    if form.validate_on_submit():
        task.name = form.title.data
        task.description = form.description.data
        task.deadline = datetime.combine(form.deadline_date.data, form.deadline_time.data)
        task.subject_id = form.subject.data
        db.session.commit()
        flash('Task has been added.', 'success')
        return redirect(url_for('tasks.schedule'))

    if request.method == 'GET':
        form.title.data = task.name
        form.description.data = task.description
        form.deadline_date.data = task.deadline
        form.deadline_time.data = task.deadline
        form.subject.data = task.subject_id

    return render_template('add_task.html', title='Add Task', form=form)


@tasks.route('/uploads/<string:filename>')
@login_required
def uploaded_file(filename):
    try:
        return send_from_directory(os.path.join(current_app.root_path, 'static/material'), filename=filename, as_attachment=False)
    except FileNotFoundError:
        abort(404)
