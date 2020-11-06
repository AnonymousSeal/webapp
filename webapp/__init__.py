from webapp.config import Config
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

# jinja2
def already_past(date):
    now = datetime.now()
    delta = date - now
    diff = delta.days + 1
    if diff < 0:
        return True
    else:
        return False

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from webapp.main.routes import main
    from webapp.tasks.routes import tasks
    from webapp.users.routes import users
    app.register_blueprint(main)
    app.register_blueprint(tasks)
    app.register_blueprint(users)

    #jinja2
    app.jinja_env.globals.update(already_past=already_past)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    return app
