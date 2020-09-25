from quickstart_app import db
from quickstart_app.models import Subject, User

def add_subject(name):
    db.session.add(Subject(name=name))
    db.session.commit()

def give_status(name, status):
    User.query.filter_by(username=name).first().status = status
    db.session.commit()
