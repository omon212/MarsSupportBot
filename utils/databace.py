import sqlite3

connect = sqlite3.connect('../support.db')
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS support (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                fullname TEXT
                )""")


async def UserRegister(user_id, fullname):
    register = cursor.execute("INSERT INTO support (user_id, fullname) VALUES (?, ?)", (user_id, fullname))
    connect.commit()
    if register:
        return True
    else:
        return False