from flask import current_app
import secrets
import os

def add_file(file, filename):
    orignial_name = file.filename
    random_hex = secrets.token_hex(4)
    _, f_ext = os.path.splitext(orignial_name)
    filename = filename + '_' + random_hex + f_ext
    file.save(os.path.join(current_app.root_path, 'static/material', filename))
    return filename
