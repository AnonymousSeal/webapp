from quickstart_app import app

def log(text, logfile='log.txt'):
    f = open(logfile,'a')
    f.write(str(text) + '\n')
    f.close()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
