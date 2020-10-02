from flask import session, current_app
import secrets
import os


def check_comment_cu_session_data(id, initial_file_cache_value=[]):
    if not 'file_chache' in session:
        session['file_chache'] = initial_file_cache_value
    if not 'staged_files_location' in session:
        session['staged_files_location'] = id
    if session['staged_files_location'] != id:
        session['staged_files_location'] = id
        session['file_chache'] = initial_file_cache_value

def add_file(file, filename):
    orignial_name = file.filename
    random_hex = secrets.token_hex(4)
    _, f_ext = os.path.splitext(orignial_name)
    filename = filename + '_' + random_hex + f_ext
    file.save(os.path.join(current_app.root_path, 'static/material', filename))
    session['file_chache'] = session['file_chache'] + [[filename, orignial_name]]
