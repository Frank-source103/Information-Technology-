from flask import Flask, render_template

app = Flask(__name__)

# Simulated content database
CONTENT = {
    "home": "Welcome to the Information Technology Department… content not added yet.",
    "about": "About page content… content not added yet.",
    "info": "Info page content… content not added yet.",
    "contact": "Contact page content… content not added yet."
}

# Function to get page content
def get_content(page):
    return CONTENT.get(page, "Content not added yet.")

# Routes
@app.route("/")
def home():
    return render_template("index.html", content=get_content("home"))

@app.route("/about")
def about():
    return render_template("about.html", content=get_content("about"))

@app.route("/info")
def info():
    return render_template("info.html", content=get_content("info"))

@app.route("/contact")
def contact():
    return render_template("contact.html", content=get_content("contact"))

# Main entry point
if __name__ == "__main__":
    # Render assigns a PORT via environment variable
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)def get_content(page):
    data = []  # or fetch from your DB/file
    return data[0] if data else "Content not added yet."
# Routes
@app.route('/')
def home():
    return render_template('index.html', content=get_content('home'))

@app.route('/about')
def about():
    return render_template('about.html', content=get_content('about'))

@app.route('/info')
def info():
    return render_template('info.html', content=get_content('info'))

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO messages (name,email,message) VALUES (?,?,?)",
                  (name,email,message))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('contact.html', content=get_content('contact'))

# Admin login
@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "admin" and password == "admin123":  # Change this for security
            session['admin'] = True
            return redirect(url_for('dashboard'))
    return render_template('admin_login.html')

# Admin dashboard
@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin'))

    pages = ['home','about','info','contact']

    if request.method == 'POST':
        page = request.form['page']
        body = request.form['body']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO content (page, body) VALUES (?,?)", (page, body))
        conn.commit()
        conn.close()

    # Get current content for all pages
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    content_dict = {}
    for page in pages:
        c.execute("SELECT body FROM content WHERE page=?", (page,))
        data = c.fetchone()
        content_dict[page] = data[0] if data else ""
    conn.close()

    return render_template('admin_dashboard.html', content_dict=content_dict, pages=pages)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)    return data[0] if data else "Content not added yet."

# Routes

@app.route('/')
def home():
    return render_template('index.html', content=get_content('home'))

@app.route('/about')
def about():
    return render_template('about.html', content=get_content('about'))

@app.route('/info')
def info():
    return render_template('info.html', content=get_content('info'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO messages (name,email,message) VALUES (?,?,?)",
                  (name,email,message))
        conn.commit()
        conn.close()

        return redirect(url_for('home'))

    return render_template('contact.html')

# Admin Login

@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "admin123":
            session['admin'] = True
            return redirect(url_for('dashboard'))

    return render_template('admin_login.html')

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin'))

    if request.method == 'POST':
        page = request.form['page']
        body = request.form['body']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("DELETE FROM content WHERE page=?", (page,))
        c.execute("INSERT INTO content (page, body) VALUES (?,?)", (page, body))
        conn.commit()
        conn.close()

    return render_template('admin_dashboard.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
