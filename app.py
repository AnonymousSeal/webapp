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
        conn, c = db.connect2db(database='database/test_database.db')
        log.comment('connected to database')
        log.comment(credentials[0] + ', ' + credentials[1])
        if db.is_password(c, credentials[0], credentials[1]):
            log.comment('correct pw')
            return redirect('/my')
        else:
            log.comment('wrong pw')
            return redirect('/login')
        log.comment('skipped')
    return render_template('login.html')

@app.route('/my')
def my():
    conn, c = db.connect2db(database='database/test_database.db')
    schedule = db.get_schedule(c)
    return render_template('my.html', schedule=schedule)

if __name__ == '__main__':
    app.run(debug=True)
