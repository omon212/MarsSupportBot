import sqlite3

connect = sqlite3.connect('../support.db')
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS support (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE,
                fullname TEXT
                )""")


async def UserRegister(user_id, fullname):
    connect = sqlite3.connect('../support.db')
    cursor = connect.cursor()
    # print(user_id,fullname)
    cursor.execute("INSERT INTO support (user_id, fullname) VALUES (?, ?)", (user_id, fullname,))
    connect.commit()
    return cursor

    # if cursor:
    #     return cursor
    # else:
    #     return False
