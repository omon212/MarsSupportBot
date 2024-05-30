import sqlite3

connect = sqlite3.connect('../support.db')
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS support (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE,
                fullname TEXT
                )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT UNIQUE,
                video TEXT,
                caption TEXT
                )""")

connect.commit()
