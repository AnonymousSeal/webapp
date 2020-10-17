class Config(object):
    # Flask settings
    SECRET_KEY = 'thisisatest'

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = config.get('sqlite:///webapp.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avids SQLAlchemy warning
