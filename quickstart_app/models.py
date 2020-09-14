from quickstart_app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    time_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)

    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    status = db.Column(db.String(20), nullable=False, default='user')

    def __repr__(self):
        return f"User('{self.username}', '{self.status}', '{self.email}', '{self.image_file}')"

class Task(db.Model):
    __tablename__ = 'schedule'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    time_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    time_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
    time_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    filename = db.Column(db.String(255), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'), nullable=False)

    def __repr__(self):
        return f"Material('{self.time_added}', '{self.filename}')"

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    time_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    time_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    title = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.Text(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'), nullable=False)

    def __repr__(self):
        return f"Comment('{self.time_added}', '{self.title}')"
