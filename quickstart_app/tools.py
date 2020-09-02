from quickstart_app import app, db

def log(text, logfile='log.txt'):
    f = open(logfile,'a')
    f.write(str(text) + '\n')
    f.close()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

from quickstart_app.models import User, Subject

def make_admin(name):
    User.query.filter_by(username=name).first().status = 'admin'
    db.session.commit()

def add_subject(name):
    db.session.add(Subject(name=name))
    db.session.commit()
