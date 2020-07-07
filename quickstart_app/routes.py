from flask_user import login_required, UserManager
from quickstart_app import app, db
from flask import render_template, request
from quickstart_app.models import User, Task

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

@app.route('/task')
@login_required    # User must be authenticated
def task():
    task = Task.query.get(request.args.get('id'))
    return render_template('task.html', task=task)
