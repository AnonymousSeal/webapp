from flask import current_app
from pathlib import Path
import os

def delete_file(filename, path, trash_path):
    try:
        Path(os.path.join(current_app.root_path, '.Trash', trash_path)).mkdir(parents=True, exist_ok=True)
        os.rename(os.path.join(current_app.root_path, path, filename), os.path.join(current_app.root_path, '.Trash', trash_path, filename))
    except:
        pass
