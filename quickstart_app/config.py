class Config(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = '#dffwr2rRF#DR^@FTFW@&y2763rygwytfe732t2eyf'

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/quickstart_app.sqlite3'    # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

    UPLOAD_FOLDER = '/Users/elias/Documents/GitRepos/webapp/quickstart_app/static/material'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'pptx', 'xlsx'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 #16 Mb
