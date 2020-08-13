from flask_user import UserMixin
from quickstart_app import db
from datetime import datetime

# Define the User data-model.
# NB: Make sure to add flask_user UserMixin !!!
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    username = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    #email_confirmed_at = db.Column(db.DateTime())

    # User information
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')

class Task(db.Model):
    __tablename__ = 'schedule'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    time_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)

class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

class Material(db.Model):
    __tablename__ = 'material'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    time_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    filename = db.Column(db.String(255), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'), nullable=False)
