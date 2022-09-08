# import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, flash
# from flask_session import Session
# from tempfile import mkdtemp

from helpers import serialize_image



# Configure application
app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Custom filter


# Configure session to use filesystem (instead of signed cookies)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///3d.db")

# Make sure API key is set


@app.after_request
def after_request(response):
    """Ensure responses aren't cashed"""
    response.headers["Cash-Control"] = "no-cashe, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cashe"
    return response



@app.route("/", methods=["GET"])
def home():
    """1 - Home page for Blog"""

    return render_template("index.html")

@app.route("/board", methods=["GET"])
def board():
    """2 - Post Board of all files posted"""

    return render_template("board.html")

@app.route("/entry", methods=["GET"])
def entry():
    """3 - Full page view containing all availible info on the the file being viewed"""

    return render_template("entry.html")
    
@app.route("/search", methods=["GET"])
def search():
    """4 - Search other 3D printing sites for files"""

    return render_template("search.html")

@app.route("/about", methods=["GET", "POST"])
def about():
    """5 - Tell about the website and offer some education resources"""

    return render_template("about.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    """6 - Allows admin to post and delete files"""

    if request.method == "POST":
        file_name = request.form.get("file_name")
        desc = request.form.get("desc")
        mtl = request.form.get("mtl")
        nzl = request.form.get("nzl")
        support = request.form.get("support")
        note = request.form.get("note")
        stl_1 = request.form.get("stl_1")
        stl_2 = request.form.get("stl_2")
        img_1 = request.form.get("img_1")
        img_2 = request.form.get("img_2")
        gcode_1 = request.form.get("gcode_1")

        # Insert data into print_info table
        db.execute("INSERT INTO print_info (file_name, desc, mtl, nzl, support, note) VALUES (?, ?, ?, ?, ?, ?)", 
            file_name, desc, mtl, nzl, support, note)
        
        # Insert data into stl table
        db.execute("INSERT INTO stl (stl_1, stl_2) VALUES (?, ?)", 
            stl_1, stl_2)

        # Insert data into img table
        db.execute("INSERT INTO img (img_1, img_2) VALUES (?, ?)", 
            img_1, img_2)

        # Insert data into gcode table
        db.execute("INSERT INTO gcode (gcode_1) VALUES (?)", 
            gcode_1)

        return render_template("admin.html")

    else:
        
        return render_template("admin.html")



# @app.route("/login", methods=["GET", "POST"])

# @app.route("/logout")

# @app.route("/register", methods=["GET", "POST"])