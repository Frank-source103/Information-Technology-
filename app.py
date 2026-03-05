from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# DATABASE INITIALIZATION
# -----------------------------
def init_db():
    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS news(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS staff(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        role TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS courses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_code TEXT,
        course_name TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS events(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# -----------------------------
# BASIC PAGES
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/info")
def info():
    return render_template("info.html")


# -----------------------------
# CONTACT PAGE
# -----------------------------
@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        print("Contact message:", name, email, message)

    return render_template("contact.html")


# -----------------------------
# NEWS PAGE
# -----------------------------
@app.route("/news")
def news():

    conn = get_db()
    posts = conn.execute("SELECT * FROM news").fetchall()
    conn.close()

    return render_template("news.html", posts=posts)


# -----------------------------
# STAFF DIRECTORY
# -----------------------------
@app.route("/staff")
def staff():

    conn = get_db()
    staff = conn.execute("SELECT * FROM staff").fetchall()
    conn.close()

    return render_template("staff.html", staff=staff)


# -----------------------------
# COURSES PAGE
# -----------------------------
@app.route("/courses")
def courses():

    conn = get_db()
    courses = conn.execute("SELECT * FROM courses").fetchall()
    conn.close()

    return render_template("courses.html", courses=courses)


# -----------------------------
# EVENTS PAGE
# -----------------------------
@app.route("/events")
def events():

    conn = get_db()
    events = conn.execute("SELECT * FROM events").fetchall()
    conn.close()

    return render_template("events.html", events=events)


# -----------------------------
# ADMIN DASHBOARD
# -----------------------------
@app.route("/admin", methods=["GET", "POST"])
def admin():

    conn = get_db()

    if request.method == "POST":

        form_type = request.form.get("form_type")

        if form_type == "news":
            title = request.form["title"]
            content = request.form["content"]

            conn.execute(
                "INSERT INTO news (title, content) VALUES (?,?)",
                (title, content)
            )

        elif form_type == "staff":
            name = request.form["name"]
            role = request.form["role"]

            conn.execute(
                "INSERT INTO staff (name, role) VALUES (?,?)",
                (name, role)
            )

        elif form_type == "course":
            code = request.form["course_code"]
            name = request.form["course_name"]

            conn.execute(
                "INSERT INTO courses (course_code, course_name) VALUES (?,?)",
                (code, name)
            )

        elif form_type == "event":
            title = request.form["title"]
            date = request.form["date"]

            conn.execute(
                "INSERT INTO events (title, date) VALUES (?,?)",
                (title, date)
            )

        conn.commit()

        return redirect("/admin")

    news = conn.execute("SELECT * FROM news").fetchall()
    staff = conn.execute("SELECT * FROM staff").fetchall()
    courses = conn.execute("SELECT * FROM courses").fetchall()
    events = conn.execute("SELECT * FROM events").fetchall()

    conn.close()

    return render_template(
        "admin.html",
        news=news,
        staff=staff,
        courses=courses,
        events=events
    )


# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
