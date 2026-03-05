from flask import Flask, render_template
import os

app = Flask(__name__)

# Page content
CONTENT = {
    "home": "Welcome to the Information Technology Department. Content not added yet.",
    "about": "About the Information Technology Department. Content not added yet.",
    "info": "Department information page. Content not added yet.",
    "contact": "Contact the Information Technology Department. Content not added yet."
}

def get_content(page):
    return CONTENT.get(page, "Content not added yet.")

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
