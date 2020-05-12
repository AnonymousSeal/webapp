import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(24) NOT NULL,
    password_hash VARCHAR(2048) NOT NULL
    )''')
c.execute('''CREATE TABLE IF NOT EXISTS schedule (
    schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_name VARCHAR(24) NOT NULL,
    time_added DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTERGER,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
    )''')
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
