from webapp.main.utils import delete_file
from flask import current_app
from flask_login import current_user
from PIL import Image
import drawSvg as draw
import numpy as np
import secrets
import random
import os

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
        delete_file(current_user.image_file, 'static/profile_pictures', 'profile_pictures')
    return picture_name

def get_picture_array():
    points = [[0,0],[0,1],[0,2],
              [1,0],[1,1],[1,2],
              [2,0],[2,1],[2,2]]
    selects = random.sample(points, 4)
    colors = ['#1E8280', '#43BF87', '#FAD157', '#F2993F', '#DB624F']
    return selects, random.choice(colors)

def generate_default_picture():
    picture_points, color = get_picture_array()
    picture_name = 'default_' + secrets.token_hex(8) + '.svg'
    picture_path = os.path.join(current_app.root_path, 'static/profile_pictures', picture_name)

    img = draw.Drawing(240, 240, origin=(-120,-120), displayInline=False)
    for y,x in picture_points:
        img.append(draw.Rectangle(30*(x), 30*(y), 30, 30, fill=color))
        img.append(draw.Rectangle(-30*(x+1), 30*(y), 30, 30, fill=color))
        img.append(draw.Rectangle(30*(x), -30*(y+1), 30, 30, fill=color))
        img.append(draw.Rectangle(-30*(x+1), -30*(y+1), 30, 30, fill=color))
    img.saveSvg(picture_path)
    return picture_name
