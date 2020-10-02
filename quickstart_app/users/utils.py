from flask import current_app
from flask_login import current_user
from quickstart_app.models import User
from PIL import Image
import secrets
import os

def get_user_by_username(name):
    return User.query.filter_by(username=name).first()

def update_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pictures', picture_name)
    output_size = (250, 250)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)
    if current_user.image_file != 'default.jpg':
        try:
            os.remove(os.path.join(current_app.root_path, 'static/profile_pictures', current_user.image_file))
        except:
            pass
    return picture_name
