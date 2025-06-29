import sqlite3

def init_db():
    conn = sqlite3.connect("db.sqlite3")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS users;")
    cur.execute("DROP TABLE IF EXISTS posts;")

    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULl,
        content TEXT NOT NULL
    )
    ''')

    # 더미 유저 생성
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("attacker", "1234"))
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("victim", "1234"))

    conn.commit()
    conn.close()
