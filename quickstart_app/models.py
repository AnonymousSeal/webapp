from quickstart_app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    time_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)

    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    status = db.Column(db.String(20), nullable=False, default='user')

    comment = db.relationship('Comment', backref='author', lazy=True, foreign_keys="Comment.author_id")

    def __repr__(self):
        return f"User('{self.username}', '{self.status}', '{self.email}', '{self.image_file}')"

class Task(db.Model):

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    time_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    time_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)

    comment = db.relationship('Comment', backref='task', lazy=True, foreign_keys="Comment.task_id")

    def __repr__(self):
        return f"Task('{self.name}', '{self.description}', '{self.deadline}')"

class Subject(db.Model):

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"Subject('{self.name}')"

class Material(db.Model):

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    time_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    time_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    filename = db.Column(db.String(255), nullable=False)

    upload_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)

    def __repr__(self):
        return f"Material('{self.time_added}', '{self.filename}')"

class Comment(db.Model):

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    time_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    time_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    title = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.Text())

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

    material = db.relationship('Material', backref='upload', lazy=True, foreign_keys="Material.upload_id")

    def __repr__(self):
        return f"Comment('{self.time_added}', '{self.title}')"
