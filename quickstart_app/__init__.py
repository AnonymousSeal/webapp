from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask import Flask
from quickstart_app.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from quickstart_app.users.routes import users
    from quickstart_app.tasks.routes import tasks
    from quickstart_app.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(tasks)
    app.register_blueprint(main)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    return app
