import sqlite3

conn = sqlite3.connect('test_database.db')
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(31) NOT NULL,
    password_hash VARCHAR(1023) NOT NULL
    )''')
c.execute('''CREATE TABLE IF NOT EXISTS subjects (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL
    )''')
c.execute('''CREATE TABLE IF NOT EXISTS schedule (
    schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
    time_added DATETIME DEFAULT CURRENT_TIMESTAMP,
    task_name VARCHAR(31) NOT NULL,
    deadline DATETIME,
    user_id INTERGER,
    subject_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
    )''')
c.execute('''CREATE TABLE IF NOT EXISTS material (
    material_id INTEGER PRIMARY KEY AUTOINCREMENT,
    material_path VARCHAR(255) NOT NULL
    )''')
c.execute('''CREATE TABLE IF NOT EXISTS uploads (
    upload_id INTEGER PRIMARY KEY AUTOINCREMENT,
    time_added DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    material_id INTEGER,
    schedule_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (material_id) REFERENCES material(material_id),
    FOREIGN KEY (schedule_id) REFERENCES schedule(schedule_id)
    )''')
c.execute('''CREATE TABLE IF NOT EXISTS comments (
    comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    comment VARCHAR (1023) NOT NULL,
    time_added DATETIME DEFAULT CURRENT_TIMESTAMP,
    reply_to INTEGER,
    schedule_id INTEGER,
    user_id INTERGER NOT NULL,
    FOREIGN KEY (reply_to) REFERENCES users(user_id),
    FOREIGN KEY (schedule_id) REFERENCES schedule(schedule_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)''')
conn.commit()
