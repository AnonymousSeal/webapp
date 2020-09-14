from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from quickstart_app.ConfigClass import ConfigClass
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)               # Create Flask app load app.config
app.config.from_object(ConfigClass)
db = SQLAlchemy(app)                # Initialize Flask-SQLAlchemy
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from quickstart_app import routes
