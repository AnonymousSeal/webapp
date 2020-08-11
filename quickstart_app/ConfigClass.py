class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = '#dffwr2rRF#DR^@FTFW@&y2763rygwytfe732t2eyf' #already changed

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/quickstart_app.sqlite3'    # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

    # Flask-User settings
    USER_APP_NAME = 'Ferienarbeitsgemeinschaft'      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = False      # Disable email authentication
    USER_ENABLE_USERNAME = True    # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = True

    UPLOAD_FOLDER = 'quickstart_app/material'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'pptx', 'xlsx'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 #16 Mb
