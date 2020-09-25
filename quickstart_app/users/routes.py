from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, redirect, url_for, flash, request, Blueprint
from quickstart_app.users.forms import RegistrationForm, LoginForm
from quickstart_app.users.utils import get_user_by_username
from quickstart_app.models import User
from quickstart_app import db, bcrypt

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('tasks.schedule'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('tasks.schedule'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('tasks.schedule'))
        flash('Login Unsuccessful. Please check email and password!', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users.route('/profile/<string:username>')
@login_required
def profile(username):
    user = get_user_by_username(username)
    image_file = url_for('static', filename='profile_pictures/' + user.image_file)
    return render_template('profile.html', title=user.username, user=user, image_file=image_file)
