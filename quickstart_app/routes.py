from quickstart_app.models import User, Task, Subject, Material
from quickstart_app.tools import allowed_file, log
from quickstart_app import app, db
from flask import render_template, request, redirect, url_for, send_from_directory, abort, flash
from flask_login import current_user
from flask_user import login_required, UserManager
from werkzeug.utils import secure_filename
from datetime import datetime
import os

user_manager = UserManager(app, db, User)   # Setup Flask-User and specify the User data-model

# The Home page is accessible to anyone
@app.route('/')
def index():
    return render_template('index.html')

# The Members page is only accessible to authenticated users via the @login_required decorator
@app.route('/schedule')
@login_required    # User must be authenticated
def schedule():
    return render_template('schedule.html', schedule=Task.query.all())

@app.route('/task', methods=['GET', 'POST'])
@login_required    # User must be authenticated
def task():

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
            db.session.add(Material(filename=filename, user_id=current_user.id, schedule_id=request.args.get('id')))
            db.session.commit()
            material = Material.query.all()

    task  = Task.query.get(request.args.get('id'))
    subject = Subject.query.get(task.subject_id)
    material = Material.query.filter(Material.schedule_id == request.args.get('id'))
    return render_template('task.html', task=task, subject=subject, material_list=material)

@app.route('/add_task', methods=['GET', 'POST'])
@login_required    # User must be authenticated
def add_task():
    if request.method == 'POST':
        db.session.add(Task(name=request.form['name'], description=request.form['description'], deadline=datetime.strptime(request.form['deadline'], '%d.%m.%Y'), user_id=current_user.id, subject_id=request.form['subject']))
        db.session.commit()
        return render_template('schedule.html', schedule=Task.query.all())
    return render_template('add_task.html', subjects=Subject.query.all())

@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    log([app.config['UPLOAD_FOLDER'], filename])
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename=filename, as_attachment=False)
    except FileNotFoundError:
        abort(404)
