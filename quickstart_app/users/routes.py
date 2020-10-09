from quickstart_app import bcrypt, db
from quickstart_app.models import User
from quickstart_app.users.forms import LoginForm, RegistrationForm, UpdateProfileForm
from quickstart_app.users.utils import get_user_by_username, update_picture
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user


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

@users.route('/profile/<string:username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = get_user_by_username(username)
    image_file = url_for('static', filename='profile_pictures/' + user.image_file)
    if user == current_user:
        form = UpdateProfileForm()
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = update_picture(form.picture.data)
                current_user.image_file = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your Profile has been updated!', 'success')
            return redirect(url_for('users.profile', username=form.username.data))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email
        return render_template('profile.html', title=user.username, user=user, image_file=image_file, form=form)
    return render_template('profile.html', title=user.username, user=user, image_file=image_file)
