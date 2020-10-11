class Config(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = '#dffwr2rRF#DR^@FTFW@&y2763rygwytfe732t2eyf'

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///webapp.sqlite3'    # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning
