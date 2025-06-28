from flask import Flask, request, session, redirect, render_template
import sqlite3

app = Flask(__name__)
app.secret_key = "super_secret_key"

def get_db():
    conn = sqlite3.connect("db.sqlite3")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    if "user_id" in session:
        return redirect("/dashboard")
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                            (username, password)).fetchone()
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect("/dashboard")
        return "로그인 실패", 401
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    return f"환영합니다, {session.get('username')}님!<br><a href='/logout'>로그아웃</a>"

@app.route("/order/<uuid>", methods=["GET", "POST"])
def view_order(uuid):
    if "user_id" not in session:
        return redirect("/login")
    conn = get_db()
    order = conn.execute("SELECT * FROM orders WHERE uuid = ?", (uuid,)).fetchone()
    if not order:
        return "주문을 찾을 수 없습니다.", 404
    
    user = conn.execute("SELECT username FROM users WHERE id = ?", (order["user_id"],)).fetchone()

    # 👇 인가 검증이 없습니다. (취약점 포인트!)
    if request.method == "POST":
        conn.execute("UPDATE orders SET is_paid = 1 WHERE uuid = ?", (uuid,))
        conn.commit()
        return render_template("result.html", username=session["username"], owner=user["username"])

    return render_template("order.html", order=order, username=session["username"])

if __name__ == "__main__":
    app.run()
