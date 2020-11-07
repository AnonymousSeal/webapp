from datetime import timedelta

class Config(object):
    # Flask settings
    SECRET_KEY = 'thisisatest'
    TESTING = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=12)

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///webapp.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avids SQLAlchemy warning
