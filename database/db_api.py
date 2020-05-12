import sqlite3
import hashlib

def connect2db(db='database.db'):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    return conn, c

def add_user(c, name, pw):
    # not a good hashing function for pws
    password_hash = hashlib.sha224(str.encode(pw)).hexdigest()
    c.execute('''INSERT INTO users (name, password_hash) VALUES (?, ?);''',
    (name, password_hash))

def get_user(c, name):
    try:
        c.execute(f'''SELECT * FROM users WHERE users.name = '{name}';''')
        user = c.fetchone()
        return user
    except:
        return None

def is_password(c, name, pw):
    user = get_user(c, name)
    if user is not None:
        this_pw_hash = hashlib.sha224(str.encode(pw)).hexdigest()
        if this_pw_hash == user[2]:
            return True
    return False

def add_schedule(c, task_name, user_id):
    pass

#conn, c = connect2db()
#add_user(c, 'testtest', 'testtest')
#conn.commit()
