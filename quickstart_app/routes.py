from quickstart_app.models import User, Task, Subject, Material, Comment
from quickstart_app.tools import allowed_file, log, make_admin, add_subject
from quickstart_app.Forms import RegistrationForm, LoginForm
from quickstart_app import app, db
from flask import render_template, request, redirect, url_for, send_from_directory, abort, flash
from flask_login import current_user
from flask_user import login_required, UserManager
from werkzeug.utils import secure_filename
from datetime import datetime
import os

user_manager = UserManager(app, db, User)   # Setup Flask-User and specify the User data-model


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/schedule')
@login_required
def schedule():
    return render_template('schedule.html', schedule=Task.query.all())

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'a@a.a' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/task/<task_id>')
@login_required
def task(task_id):
    task  = Task.query.get(task_id)
    subject = Subject.query.get(task.subject_id)
    material = Material.query.filter(Material.schedule_id == task_id)
    comments = Comment.query.filter(Comment.schedule_id == task_id)
    return render_template('task.html', task=task, subject=subject)

@app.route('/add_comment/<task_id>', methods=['GET', 'POST'])
@login_required    # User must be authenticated
def add_comment(task_id):
    if request.method == 'POST':
        db.session.add(Comment(title=request.form['title'], comment=request.form['comment'], user_id=current_user.id, schedule_id=task_id))
        db.session.commit()

        return redirect(url_for('task', task_id=task_id))
    return render_template('add_comment.html')

@app.route('/add_task', methods=['GET', 'POST'])
@login_required    # User must be authenticated
def add_task():
    if request.method == 'POST':
        db.session.add(Task(name=request.form['name'], description=request.form['description'], deadline=datetime.strptime(request.form['deadline'], '%d.%m.%Y'), user_id=current_user.id, subject_id=request.form['subject']))
        db.session.commit()

        return redirect(url_for('schedule'))
    return render_template('add_task.html', subjects=Subject.query.all())

@app.route('/upload_file/<task_id>', methods=['GET', 'POST'])
@login_required    # User must be authenticated
def upload_file(task_id):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            db.session.add(Material(filename=filename, user_id=current_user.id, schedule_id=task_id))
            db.session.commit()

        return redirect(url_for('task', task_id=task_id))
    return render_template('upload_file.html', subjects=Subject.query.all())

@app.route('/uploads/<filename>')
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
    if user.status != 'admin':
        flash('Only admins can view this page.')
        return redirect(url_for('profile'))

    if request.method == 'POST':
        add_subject(request.form['name'])
    admins = User.query.filter_by(status='admin').all()
    #users = User.query.filter_by(status='user').all()
    return render_template('admin_page.html', title='Admin Page', admins=admins)
