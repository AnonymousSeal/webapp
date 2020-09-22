from quickstart_app import db, app
from quickstart_app.models import User, Subject

def add_subject(name):
    db.session.add(Subject(name=name))
    db.session.commit()

def make_admin(name):
    User.query.filter_by(username=name).first().status = 'admin'
    db.session.commit()
