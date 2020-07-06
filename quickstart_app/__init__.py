from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from quickstart_app.ConfigClass import ConfigClass

app = Flask(__name__)               # Create Flask app load app.config
app.config.from_object(ConfigClass)
db = SQLAlchemy(app)                # Initialize Flask-SQLAlchemy

from quickstart_app import routes
