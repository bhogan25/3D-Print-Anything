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
# OLD LOCATION: /mnt/c/users/Ben Hogan/documents/CS 2022/CS50 - Harvard/Projects/final_project/cs50-final-project/static/<final_location_here>
# ONE DRIVE LOCATION: /mnt/c/Users/Ben Hogan/OneDrive/Documents/CS 2022/CS50 - Harvard/Projects/Final_Project/cs50-final-project

app.config["IMAGE_UPLOADS"] = "/mnt/c/Users/Ben Hogan/OneDrive/Documents/CS 2022/CS50 - Harvard/Projects/Final_Project/cs50-final-project/static/img"
app.config['STL_UPLOADS'] = "/mnt/c/Users/Ben Hogan/OneDrive/Documents/CS 2022/CS50 - Harvard/Projects/Final_Project/cs50-final-project/static/stl"
app.config['GCODE_UPLOADS'] = "/mnt/c/Users/Ben Hogan/OneDrive/Documents/CS 2022/CS50 - Harvard/Projects/Final_Project/cs50-final-project/static/gcode"

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
                return apology("Unable not process request", 400)
  
            print(f'{extention.upper()} FILE ---"{media}"--- BEING RETRIEVED')
            return send_from_directory(path, media, as_attachment=True)

    else: 
        fileList = db.execute("SELECT title, desc, tstp, stl_filename, img_filename, gcode_filename, post_key FROM print_info")
        if fileList:
            print('Fetched files from database:')
            print(fileList)
        
        else:
            print("No Files were retreived from database")
        
        return render_template("board.html", fileList=fileList)
    

@app.route("/entry", methods=["GET", "POST"])
def entry():
    """3 - Full page view containing all availible info on the the file being viewed"""

    # Download a file from /entry
    if request.method == "POST":
        try: 
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
                return apology("Unable not process request", 400)
  
            print(f'{extention.upper()} FILE ---"{media}"--- BEING RETRIEVED')
            return send_from_directory(path, media, as_attachment=True)
        
        except:
            return apology("Unable not process request", 400)


    # View a post
    else: 
        post_key = request.args.get('pk')
        print(F"FETCHING DATA FOR POST: {post_key}")

    try:
        postDataList = db.execute("SELECT title, desc, tstp, mtl, nzl, support, note, stl_filename, img_filename, gcode_filename FROM print_info WHERE post_key = ?", post_key)
        postData = postDataList[0]
        print('FETCHED DATA FROM DATABASE:')
        print(postData)
        return render_template("entry.html", postData=postData)

    except:
        return apology("Unable not process request", 400) 
   
 
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
            post_key = token_hex(13)

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
            print("SAVING FORM DATA ---------------------------------------->")
            try:
                db.execute(f"INSERT INTO print_info (title, desc, tstp, post_key) VALUES(?, ?, ?, ?)",title, desc, tstp, post_key)
            
            except:
                return apology('An error occured while saving form data to database', 400)

            # SAVE FILES TO FOLDER & FILENAMES TO DATABASE
            print("SAVING FILES ---------------------------------------->")
            try:
                for fileDict in recieved_files:
                    print(f"SAVING -- '{fileDict['filename']}' -- TO FILE SYSTEM")
                    fileDict['requestObj'].save(os.path.join(fileDict['uploadPath'], fileDict['filename']))
                    
                    print(f"SAVING -- '{fileDict['filename']}' -- TO DATABASE")
                    db.execute(f"UPDATE print_info SET {fileDict['column']}='{fileDict['filename']}' WHERE post_key='{post_key}'")
            
            except:
                # TODO Delete info from form submitted if all files cannot be submitted
                db.execute(f"DELETE FROM print_info WHERE post_key='{post_key}'")
                return apology('An error occured while saving files to database', 400)
        
        else:
            return apology('No form data was submitted', 400)

        return render_template("admin.html", recieved_files=recieved_files)
    else: 
        return render_template("admin.html")


# @app.route("/login", methods=["GET", "POST"])

# @app.route("/logout")

# @app.route("/register", methods=["GET", "POST"])