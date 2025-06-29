from flask import Flask, request, session, redirect, render_template, make_response
import sqlite3
import base64

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

            raw_token = f"{username} / {password}"
            encoded_token = base64.b64encode(raw_token.encode()).decode()

            resp = make_response(redirect("/dashboard"))
            resp.set_cookie("token", encoded_token, httponly=False)

            return resp
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
    
    conn = get_db()
    posts = conn.execute("SELECT * FROM posts ORDER BY id DESC").fetchall()
    conn.close()
    
    return render_template("dashboard.html", username=session.get("username"), posts=posts)

# 글 작성 페이지 및 처리
@app.route("/post/new", methods=["GET", "POST"])
def new_post():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        if title and content:
            conn = get_db()
            conn.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
            conn.commit()
            conn.close()
            return redirect("/dashboard")
        else:
            return "제목과 내용을 모두 입력하세요.", 400
    return render_template("new_post.html")

# 글 읽기 페이지
@app.route("/post/<int:post_id>")
def view_post(post_id):
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    conn.close()
    if not post:
        abort(404)
    return render_template("view_post.html", post=post)

if __name__ == "__main__":
    app.run()
