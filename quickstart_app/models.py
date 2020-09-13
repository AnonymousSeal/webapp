from flask_user import UserMixin
from quickstart_app import db
from datetime import datetime

# Define the User data-model.
# NB: Make sure to add flask_user UserMixin !!!
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    # TODO: time_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    username = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')

    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    status = db.Column(db.String(20), nullable=False, default='user')

    # User information
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')

    def __repr__(self):
        return f"User('{self.username}', '{self.status}', '{self.image_file}')"

class Task(db.Model):
    __tablename__ = 'schedule'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    time_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # TODO:  time_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)

    material = db.relationship('Material', backref='uploads', lazy=True)
    comments = db.relationship('Comment', backref='comments', lazy=True)

    def __repr__(self):
        return f"Task('{self.name}', '{self.description}', '{self.deadline}')"

class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"Subject('{self.name}')"

class Material(db.Model):
    __tablename__ = 'material'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    time_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # TODO:  time_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    filename = db.Column(db.String(255), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'), nullable=False)

    def __repr__(self):
        return f"Material('{self.time_added}', '{self.filename}')"

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    time_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # TODO:  time_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    title = db.Column(db.String(60), nullable=False)
    comment = db.Column(db.String(510), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'), nullable=False)

    def __repr__(self):
        return f"Comment('{self.time_added}', '{self.title}', '{self.comment}')"
