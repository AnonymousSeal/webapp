from flask_login import current_user, login_required
from flask import render_template, redirect, url_for, request, Blueprint
from quickstart_app.models import User, Task, Subject
from quickstart_app.main.utils import add_subject
from quickstart_app import db
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/config', methods=['GET', 'POST'])
@login_required
def config():
    user = User.query.get_or_404(current_user.id)
    if user.status == 'user':
        abort(403)

    if request.method == 'POST':
        add_subject(request.form['name'])
    admins = User.query.filter_by(status='admin').all()
    god_mode = User.query.filter_by(status='god_mode').all()
    return render_template('config.html', title='Config', admins=admins+god_mode)
