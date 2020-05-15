from flask import Flask, render_template, url_for, request, redirect
import debug.debug_tools as log
import database.db_api as db

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST','GET'])
#login still needs improvement (flask user handling) + User class
def login():
    if request.method == 'POST':
        credentials = [request.form['email'],request.form['password']]
        _, c = db.connect2db(database='database/test_database.db')
        log.comment('connected to database')
        log.comment(credentials[0] + ', ' + credentials[1])
        if db.is_password(c, credentials[0], credentials[1]):
            log.comment('correct pw')
            return redirect(url_for('schedule'))
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/schedule')
def schedule():
    _, c = db.connect2db(database='database/test_database.db')
    schedule = db.get_schedule(c)
    return render_template('schedule.html', schedule=schedule)

@app.route('/task')
def task():
    task_id = request.args.get('id')
    _, c = db.connect2db(database='database/test_database.db')
    task = db.get_task_by_id(c, task_id)
    subject = db.get_subject_by_id(c, task[4])
    return render_template('task.html', task=task, subject=subject)

if __name__ == '__main__':
    app.run(debug=True)
