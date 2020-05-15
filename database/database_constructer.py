import sqlite3

conn = sqlite3.connect('test_database.db')
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS users (
    email VARCHAR(255) PRIMARY KEY,
    name VARCHAR(24) NOT NULL,
    password_hash VARCHAR(2048) NOT NULL
    )''')
c.execute('''CREATE TABLE IF NOT EXISTS schedule (
    schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
    time_added DATETIME DEFAULT CURRENT_TIMESTAMP,
    task_name VARCHAR(24) NOT NULL,
    deadline DATETIME,
    user_id INTERGER,
    subject_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
    )''')
#c.execute('''CREATE TABLE IF NOT EXISTS subjects (
#    subject_id AUTOINCREMENT PRIMARY KEY,
#    name VARCHAR(10)''')
#c.execute('''CREATE TABLE IF NOT EXISTS material (
#    material_id INTEGER PRIMARY KEY AUTOINCREMENT,
#    material_path
#    )''')
#c.execute('''CREATE TABLE IF NOT EXISTS uploads (
#    upload_id INTEGER PRIMARY KEY AUTOINCREMENT,
#    time_added,
#    time_modified,
#    user_id,
#    material_id,
#    schedule_id
#    )''')
#c.execute('''CREATE TABLE IF NOT EXISTS comments (
#    comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
#    comment,
#    time_added,
#    reply_to,
#    schedule_id,
#    user_id
#)''')
conn.commit()
