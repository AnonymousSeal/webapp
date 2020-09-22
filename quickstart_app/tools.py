from quickstart_app import db, app
from quickstart_app.models import User, Subject

def add_subject(name):
    db.session.add(Subject(name=name))
    db.session.commit()

def give_status(name, status):
    User.query.filter_by(username=name).first().status = status
    db.session.commit()

def get_user_by_username(name):
    return User.query.filter_by(username=name).first()
