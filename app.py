import os

from secrets import token_hex
from datetime import datetime
from cs50 import SQL
from flask import Flask, redirect, render_template, request, flash, send_file, url_for, send_from_directory
from werkzeug.wrappers import Response
from werkzeug.utils import secure_filename
from helpers import accepted_extension, convertToBinary, apology

# Configure application
app = Flask(__name__)

# TODO Configure CS50 Library to use SQLite database
db = SQL("sqlite:///3d.db")

# Establish allowed img extentions
ALLOWED_IMAGE_EXTENSIONS = {'svg', 'png', 'jpg', 'jpeg'}

# Configure Upload Paths
app.config["IMAGE_UPLOADS"] = "/mnt/c/users/Ben Hogan/documents/CS 2022/CS50 - Harvard/Projects/Mini_Project_DB/static/img"
app.config['STL_UPLOADS'] = "/mnt/c/users/Ben Hogan/documents/CS 2022/CS50 - Harvard/Projects/Mini_Project_DB/static/stl"
app.config['GCODE_UPLOADS'] = "/mnt/c/users/Ben Hogan/documents/CS 2022/CS50 - Harvard/Projects/Mini_Project_DB/static/gcode"

# Cashe Control
@app.after_request
def after_request(response):
    """Ensure responses aren't cashed"""
    response.headers["Cashe-Control"] = "no-cashe, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cashe"
    return response


@app.route("/", methods=["GET"])
def home():
    """1 - Home page for Blog"""

    return render_template("index.html")

@app.route("/board", methods = ["GET", "POST"])
def board():
    """2 - Post Board of all files posted"""
    if request.method == "POST":
        if request.form:
            media = request.form.get('download')
            extention = media.rsplit('.', 1)[1].lower()

            if extention == 'stl':
                path = app.config['STL_UPLOADS']

            elif extention in ALLOWED_IMAGE_EXTENSIONS:
                path = app.config['IMAGE_UPLOADS']

            elif extention == 'gcode':
                path = app.config['GCODE_UPLOADS']
                
            else:
                return redirect("download")
  
            print(f'{extention.upper()} FILE ---"{media}"--- BEING RETRIEVED')
            return send_from_directory(path, media, as_attachment=True)

    else: 
        # TODO - Be selective with which data to display.  More will be displayed on the entry page.
        fileList = db.execute("SELECT title, desc, tstp, stl_filename, img_filename, gcode_filename FROM print_info")
        print('Fetched files from database:')
        print(fileList)
        return render_template("board.html", fileList=fileList)
    

@app.route("/entry", methods=["GET"])
def entry():
    """3 - Full page view containing all availible info on the the file being viewed"""
    # TODO - Display all info about print and all files 

    fileList = db.execute("SELECT title, desc, tstp, mtl, nzl, support, note, stl_filename, img_filename, gcode_filename FROM print_info")
    print('Fetched data from database:')
    print(fileList)
    return render_template("entry.html", fileList=fileList)
   
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
    """Page to test uploading files to project folder"""
    if request.method == "POST":
        """1) Validate Form Data
           2) Validate File Data"""
        

        if request.form:
            """Check 1) [ON HOLD] - Form data name for each input are correct
                     2) From values for each input are present"""

            # 1) DO (if users will be uploading files)

            # 2)
            for input in request.form:
                if request.form[input] == "":
                    return apology('Please complete all text fields of the form', 400)

            # Assign form attributes
            title = request.form.get('title')
            desc = request.form.get('desc')
            tstp = datetime.now()
            upload_key = token_hex(13)

            recieved_files = []

            if request.files:
                """Check 1) [ON HOLD] Data names are correct
                        2) STL filename is present and has .stl extention
                        3) File type for each file is is valid
                        4) Size of each file is acceptable"""
                
                # 1) DO (if users will be uploading files) - reject all and reload page if any form names are uknown, missmatched with filename extention, etc
                
                # 2) & 3)
                

                for file in request.files:
                    filename = request.files[file].filename
                    inputName = request.files[file].name

                    if inputName == 'stl_1':
                        if filename == '':
                            return apology('An STL file must be included to upload post', 400)
                        ext = 'stl'
                        column = 'stl_filename'
                        uploadPath = app.config["STL_UPLOADS"]
                        
                    elif inputName == 'img_1':
                        ext = ALLOWED_IMAGE_EXTENSIONS
                        column = 'img_filename'
                        uploadPath = app.config["IMAGE_UPLOADS"]

                    elif inputName == 'gcode_1':
                        ext = 'gcode'
                        column = 'gcode_filename'
                        uploadPath = app.config["GCODE_UPLOADS"]

                    else:
                        return redirect(url_for('admin'))

                    if filename != '':
                        if not accepted_extension(filename, ext):
                            return apology(f'Unsupported file type submitted', 400)
                        
                        else:
                            dict = {
                                'inputName': inputName, 
                                'filename': filename,
                                'column': column,
                                'requestObj': request.files[file],
                                'uploadPath': uploadPath
                                }

                            recieved_files.append(dict)

            else: 
                return apology('No files were submitted', 400)

            # 4) TODO Check file size before saving file

            print(recieved_files)

            # SAVE FORM DATA
            print(recieved_files)

            print("SAVING FORM DATA ---------------------------------------->")
            db.execute(f"INSERT INTO print_info (title, desc, tstp, upload_key) VALUES(?, ?, ?, ?)",title, desc, tstp, upload_key)

            # SAVE FILES TO FOLDER & FILENAMES TO DATABASE
            print("SAVING FILES ---------------------------------------->")
            for fileDict in recieved_files:
                print(f"SAVING -- '{fileDict['filename']}' -- TO FILE SYSTEM")
                fileDict['requestObj'].save(os.path.join(fileDict['uploadPath'], fileDict['filename']))
                
                print(f"SAVING -- '{fileDict['filename']}' -- TO DATABASE")
                db.execute(f"UPDATE print_info SET {fileDict['column']}='{fileDict['filename']}' WHERE upload_key='{upload_key}'")
        
        else:
            return apology('No form data was submitted', 400)

        return render_template("admin.html", recieved_files=recieved_files)
    else: 
        return render_template("admin.html")


# @app.route("/login", methods=["GET", "POST"])

# @app.route("/logout")

# @app.route("/register", methods=["GET", "POST"])