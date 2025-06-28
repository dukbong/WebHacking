import sqlite3

def init_db():
    conn = sqlite3.connect("db.sqlite3")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uuid TEXT,
        user_id INTEGER,
        item TEXT,
        price INTEGER,
        is_paid INTEGER DEFAULT 0
    );
    """)

    cur.execute("DELETE FROM users;")
    cur.execute("DELETE FROM orders;")

    # 더미 유저 생성
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("attacker", "1234"))
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("victim", "1234"))

    attacker = conn.execute("SELECT id FROM users WHERE username = ?", ('attacker',)).fetchone()

    order_uuid = "c42ba5b5-c572-42fa-a9c6-ed8dc2ae842e"
    cur.execute("INSERT INTO orders (uuid, user_id, item, price) VALUES (?, ?, ?, ?)", 
                (order_uuid, attacker["id"], "AirPods Pro", 299000))

    conn.commit()
    conn.close()
