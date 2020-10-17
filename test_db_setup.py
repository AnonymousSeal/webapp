from webapp import bcrypt, db
from webapp.models import *
from run import app

db.init_app(app)
bcrypt.init_app(app)

with app.app_context():
    db.create_all()
    db.session.add(User(username='aa', email='a@a.a', password=bcrypt.generate_password_hash('a').decode('utf-8'), status='god_mode'))
    db.session.add(User(username='bb', email='b@b.b', password=bcrypt.generate_password_hash('b').decode('utf-8'), status='editor'))
    db.session.add(User(username='cc', email='c@c.c', password=bcrypt.generate_password_hash('c').decode('utf-8'), status='user'))
    db.session.commit()
