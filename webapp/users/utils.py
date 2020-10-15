from webapp.main.utils import delete_file
from flask import current_app
from flask_login import current_user
from PIL import Image
import secrets
import os

def update_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pictures', picture_name)
    img = Image.open(form_picture)
    # square selection
    x,y = img.size
    print(x,y)
    new_size = min(x,y)
    if x > y:
        img = img.crop(((x-y)/2,0,(x+y)/2,y))
    else:
        img = img.crop((0,(y-x)/2,x,(y+x)/2))
    # thumbnail
    output_size = (250, 250)
    img.thumbnail(output_size)
    img.save(picture_path)
    if current_user.image_file != 'default.jpg':
        delete_file(current_user.image_file, 'static/profile_pictures', 'profile_pictures')
    return picture_name
