from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "pptx", "zip"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ----------------------------
# DATABASE CONNECTION
# ----------------------------

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# ----------------------------
# DATABASE INITIALIZATION
# ----------------------------

def init_db():
    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        position TEXT,
        photo TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        material TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# ----------------------------
# BASIC PAGES
# ----------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/info")
def info():
    return render_template("info.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


# ----------------------------
# STAFF DIRECTORY
# ----------------------------

@app.route("/staff")
def staff():
    conn = get_db()
    staff = conn.execute("SELECT * FROM staff").fetchall()
    conn.close()
    return render_template("staff.html", staff=staff)


# ----------------------------
# COURSES PAGE
# ----------------------------

@app.route("/courses")
def courses():
    conn = get_db()
    courses = conn.execute("SELECT * FROM courses").fetchall()
    conn.close()
    return render_template("courses.html", courses=courses)


# ----------------------------
# DOWNLOAD COURSE MATERIAL
# ----------------------------

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


# ----------------------------
# NEWS PAGE
# ----------------------------

@app.route("/news")
def news():
    conn = get_db()
    posts = conn.execute("SELECT * FROM news").fetchall()
    conn.close()
    return render_template("news.html", posts=posts)


# ----------------------------
# ADMIN LOGIN
# ----------------------------

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid login")

    return render_template("admin_login.html")


# ----------------------------
# ADMIN DASHBOARD
# ----------------------------

@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    conn = get_db()

    staff = conn.execute("SELECT * FROM staff").fetchall()
    courses = conn.execute("SELECT * FROM courses").fetchall()
    news = conn.execute("SELECT * FROM news").fetchall()

    conn.close()

    return render_template("dashboard.html", staff=staff, courses=courses, news=news)


# ----------------------------
# ADD STAFF
# ----------------------------

@app.route("/add_staff", methods=["POST"])
def add_staff():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    name = request.form["name"]
    position = request.form["position"]

    photo = request.files["photo"]

    filename = secure_filename(photo.filename)
    photo.save(os.path.join("static/staff", filename))

    conn = get_db()
    conn.execute(
        "INSERT INTO staff (name, position, photo) VALUES (?, ?, ?)",
        (name, position, filename)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))


# ----------------------------
# ADD COURSE
# ----------------------------

@app.route("/add_course", methods=["POST"])
def add_course():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    title = request.form["title"]
    description = request.form["description"]

    material = request.files["material"]

    filename = secure_filename(material.filename)
    material.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    conn = get_db()
    conn.execute(
        "INSERT INTO courses (title, description, material) VALUES (?, ?, ?)",
        (title, description, filename)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))


# ----------------------------
# ADD NEWS
# ----------------------------

@app.route("/add_news", methods=["POST"])
def add_news():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    title = request.form["title"]
    content = request.form["content"]

    conn = get_db()
    conn.execute(
        "INSERT INTO news (title, content) VALUES (?, ?)",
        (title, content)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))


# ----------------------------
# LOGOUT
# ----------------------------

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("home"))


# ----------------------------
# RUN SERVER
# ----------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
