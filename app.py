import os

from secrets import token_hex
from datetime import datetime
from cs50 import SQL
from flask import Flask, redirect, render_template, request, flash, send_file, url_for, send_from_directory
from werkzeug.wrappers import Response
from werkzeug.utils import secure_filename
from helpers import accepted_extension, apology

# Configure application
app = Flask(__name__)

# TODO Configure CS50 Library to use SQLite database
db = SQL("sqlite:///3d.db")

# Establish allowed img extentions
ALLOWED_IMAGE_EXTENSIONS = {'svg', 'png', 'jpg', 'jpeg'}

# Configure Upload Paths
# OLD LOCATION: /mnt/c/users/Ben Hogan/documents/CS 2022/CS50 - Harvard/Projects/final_project/cs50-final-project/static/<final_location_here>
# ONE DRIVE LOCATION: /mnt/c/Users/Ben Hogan/OneDrive/Documents/CS 2022/CS50 - Harvard/Projects/Final_Project/cs50-final-project

app.config['STL_UPLOADS'] = "/mnt/c/Users/Ben Hogan/OneDrive/Documents/CS 2022/CS50 - Harvard/Projects/Final_Project/cs50-final-project/static/stl"
app.config["IMAGE_UPLOADS"] = "/mnt/c/Users/Ben Hogan/OneDrive/Documents/CS 2022/CS50 - Harvard/Projects/Final_Project/cs50-final-project/static/img"
app.config['GCODE_UPLOADS'] = "/mnt/c/Users/Ben Hogan/OneDrive/Documents/CS 2022/CS50 - Harvard/Projects/Final_Project/cs50-final-project/static/gcode"
pathList = [app.config['STL_UPLOADS'], app.config["IMAGE_UPLOADS"], app.config['GCODE_UPLOADS']]

app.config['DEFAULT_IMAGE'] = "static/img/default-no-image.png"



# Cashe Control
@app.after_request
def after_request(response):
    """Ensure responses aren't cashed"""
    response.headers["Cashe-Control"] = "no-cashe, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cashe"
    return response


@app.route("/", methods=["GET"])
def index():
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
  
            print(f'{extention.upper()} FILE ---"{media}"--- BEING RETRIEVED')
            return send_from_directory(path, media, as_attachment=True)

    else: 
        print('________________REQUEST________________')
        print(request)
        print('________________REQUEST.HEADER________________REQUEST')
        print(request.headers)

        fileList = db.execute("SELECT title, desc, tstp, stl_filename, img_filename, gcode_filename, post_key FROM print_info")
        
        if fileList:
            # print('Fetched files from database:')
            # print(fileList)
            print(f"defaultImage path = {app.config['DEFAULT_IMAGE']}")
        else:
            print("No Files were retreived from database")
        
        return render_template("board.html", defaultImage=app.config['DEFAULT_IMAGE'], fileList=fileList)
    

@app.route("/entry", methods=["GET", "POST"])
def entry():
    """3 - Full page view containing all availible info on the the file being viewed"""

    # Download a file from /entry page
    if request.method == "POST":
        try: 
            if request.form:
                media = request.form.get('download')
                extention = media.rsplit('.', 1)[1].lower()

                if extention == 'stl':
                    path = app.config['STL_UPLOADS']
                
                elif extention == 'gcode':
                    path = app.config['GCODE_UPLOADS']
                
                else:
                    return apology("Client request for files not allowed", 400)
  
            print(f'{extention.upper()} FILE ---"{media}"--- BEING RETRIEVED')
            return send_from_directory(path, media, as_attachment=True)
        
        except:
            return apology("Client request bad", 400)


    # View a post from board
    else: 
        post_key = request.args.get('pk')
        print(F"FETCHING DATA FOR POST: {post_key}")

        try:
            postDataList = db.execute("SELECT title, desc, tstp, mtl, nzl, support, note, stl_filename, img_filename, gcode_filename FROM print_info WHERE post_key = ?", post_key)
            postData = postDataList[0]
            print('FETCHED DATA FROM DATABASE:')
            print(postData)
            return render_template("entry.html", defaultImage=app.config['DEFAULT_IMAGE'], postData=postData)

        except:
            return apology("Unable to retreive data from database", 400) 
   
 
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
    """Page to control content uploaded to website"""

    # Test Database connection and pull content
    try: 
        fileList = db.execute("SELECT title, desc, tstp, mtl, support, nzl, note, post_key, stl_filename, img_filename, gcode_filename FROM print_info")
                    
    except:
        print("No Files were retreived from database")
    
    # On form Submission
    if request.method == "POST":

        # Distinguish between UPLOAD FROM and DELETE FROM via requested content
        if 'post_key' not in request.form:
            '''UPLOAD FROM'''

            print("_______________request.form is printed below ___________________")
            print(request.form)
            
            # Check for blank text input
            if request.form.get("title") == '' or request.form.get('desc') == '':
                return apology('Please fill out required text fields of the form', 400)

            # Get form data and create tstp & post_key
            title = request.form.get('title')
            desc = request.form.get('desc')
            tstp = datetime.now()
            mtl = request.form.get('mtl')
 
            support = "None"
            if request.form.get('support'):
                support = 'Yes'

            nzl = request.form.get('nzl')
            note = request.form.get('note')
            post_key = token_hex(13)

            recieved_files = []
 
            if request.files:
                """Check 1) [ON HOLD] Data names are correct
                        2) STL filename is present and has .stl extention
                        3) File ext for each file is is valid
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
                db.execute(f"INSERT INTO print_info (title, desc, tstp, mtl, support, nzl, note, post_key) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", title, desc, tstp, mtl, support, nzl, note, post_key)
            
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

                fileList = db.execute("SELECT title, desc, tstp, mtl, support, nzl, note, post_key, stl_filename, img_filename, gcode_filename FROM print_info")
                return render_template('admin.html', fileList=fileList)

            except: 
                # Delete info from form submitted if all files cannot be submitted
                fileList = delete(post_key)
                return apology('An error occured while saving files to database', 400)

        else:
            '''DELETE FROM'''
            post_key = request.form.get("post_key")
            fileList = delete(post_key)
            return render_template("admin.html", fileList=fileList)

    else:
        return render_template("admin.html", defaultImage=app.config["DEFAULT_IMAGE"], fileList=fileList)

def delete(post_key):
    '''Delete entry and refetch database data'''
    try:
        postFileRaw = db.execute(f"SELECT stl_filename, img_filename, gcode_filename FROM print_info WHERE post_key='{post_key}'")
        postFilenames = list(postFileRaw[0].values())
        print(postFilenames)
        print(pathList)
        
        # Only execute this part if files are present in database (thus files present in static dirs)
        postTuples = tuple(zip(pathList, postFilenames))
        for item in postTuples: 
            if item[1] != None:
                print(f'Removing FILE {item[1]} from DIRECTORY {item[0]}')
                path = os.path.join(item[0], item[1])
                os.remove(path)

        db.execute(f"DELETE FROM print_info WHERE post_key='{post_key}'")
        return db.execute("SELECT title, desc, tstp, mtl, support, nzl, note, post_key, stl_filename, img_filename, gcode_filename FROM print_info")
        
    except:
        return apology("Unable to delete entry, please try again", 400)

