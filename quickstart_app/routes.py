from quickstart_app.models import User, Task, Subject, Material, Comment
from quickstart_app.tools import add_subject, allowed_file, make_admin
from quickstart_app.Forms import RegistrationForm, LoginForm, CommentForm
from quickstart_app import app, db, bcrypt
from flask import render_template, request, redirect, url_for, send_from_directory, abort, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from datetime import datetime
import os


@app.route('/')
@app.route('/home')
@app.route('/schedule')
@login_required
def schedule():
    return render_template('schedule.html', title='Schedule', schedule=Task.query.all())

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('schedule'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('schedule'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('schedule'))
        flash('Login Unsuccessful. Please check email and password!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/task/<int:task_id>')
@login_required
def task(task_id):
    task  = Task.query.get(task_id)
    subject = Subject.query.get(task.subject_id)
    return render_template('task.html', title=task.name, task=task, subject=subject)

@app.route('/add_comment/<int:task_id>', methods=['GET', 'POST'])
@login_required
def add_comment(task_id):
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(title=form.title.data, comment=form.content.data, author_id=current_user.id, task_id=task_id)
        db.session.add(comment)
        db.session.commit()
        
        return redirect(url_for('task', task_id=task_id))
    return render_template('add_comment.html', title='Add Comment', form=form)

@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        db.session.add(Task(name=request.form['name'], description=request.form['description'], deadline=datetime.strptime(request.form['deadline'], '%d.%m.%Y'), user_id=current_user.id, subject_id=request.form['subject']))
        db.session.commit()

        return redirect(url_for('schedule'))
    return render_template('add_task.html', title='Add Task', subjects=Subject.query.all())

@app.route('/uploads/<string:filename>')
@login_required
def uploaded_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename=filename, as_attachment=False)
    except FileNotFoundError:
        abort(404)

@app.route('/profile')
@login_required
def profile():
    user = User.query.get(current_user.id)
    image_file = url_for('static', filename='profile_pictures/' + current_user.image_file)
    return render_template('profile.html', title='Profile', user=user, image_file=image_file)

@app.route('/admin_page', methods=['GET', 'POST'])
@login_required
def admin_page():
    user = User.query.get(current_user.id)
    if user.status == 'user':
        flash('Only admins can view this page.', 'info')
        return redirect(url_for('profile'))

    if request.method == 'POST':
        add_subject(request.form['name'])
    admins = User.query.filter_by(status='admin').all()
    god_mode = User.query.filter_by(status='god_mode').all()
    #users = User.query.filter_by(status='user').all()
    return render_template('admin_page.html', title='Admin Page', admins=admins+god_mode)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
