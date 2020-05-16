import sqlite3
import hashlib

#------ connection ------#

def connect2db(database='database.db'):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    return conn, c

#------ user ------#

def add_user(c, email, name, pw):
    # not a good hashing function for pws
    password_hash = hashlib.sha224(str.encode(pw)).hexdigest()
    c.execute('''INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?);''',
    (email, name, password_hash))

def get_user(c, email):
    try:
        c.execute(f'''SELECT * FROM users WHERE users.email = '{email}';''')
        user = c.fetchone()
        return user
    except:
        return None

def is_password(c, email, pw):
    user = get_user(c, email)
    if user is not None:
        this_pw_hash = hashlib.sha224(str.encode(pw)).hexdigest()
        if this_pw_hash == user[2]:
            return True
    return False

#------ schedule ------#

def add_schedule_task(c, task_name, deadline, user_id, subject_id):
    c.execute('''INSERT INTO schedule (task_name, deadline, user_id, subject_id) VALUES (?, ?, ?, ?);''',
    (task_name, deadline, user_id, subject_id))

def get_schedule(c):
    c.execute('''SELECT * FROM schedule''')
    return c.fetchall()

def get_task_by_id(c, id):
    c.execute(f'''SELECT * FROM schedule WHERE schedule_id = '{id}';''')
    return c.fetchone()

#------ subject ------#

def add_subject(c, name):
    c.execute(f'''INSERT INTO subjects (name) VALUES ('{name}');''')

def get_subject_by_id(c, id):
    c.execute(f'''SELECT * FROM subjects WHERE subject_id = '{id}';''')
    return c.fetchone()[1]
