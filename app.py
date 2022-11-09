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

# Configure SQLite database
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
    """Home page for Blog"""
    recentsQuery = """
        SELECT title, desc, tstp, stl_filename, img_filename, gcode_filename, post_key 
        FROM print_info
        WHERE id IN
        (
            SELECT id
            FROM print_info
            ORDER BY id DESC
            LIMIT 4
        )
        ORDER BY id DESC
        """
    try:
        recentsQueryData = db.execute(recentsQuery)
    
    except:
        print('UNABLE TO EXECUTE recentsQuery')

    return render_template("index.html", defaultImage=app.config['DEFAULT_IMAGE'], recentsQueryData=recentsQueryData)


@app.route("/board", methods = ["GET"])
def board():
    """Post Board of all files posted"""
    if request.method == "GET":
        # DISPLAY ALL POSTS ON BOARD
        boardQuery = """SELECT title, desc, tstp, stl_filename, img_filename, gcode_filename, post_key 
                        FROM print_info
                        """
        try:
            boardQueryData = db.execute(boardQuery)

        except: 
            print("UNABLE TO EXECUTE boardQuery")

        return render_template("board.html", defaultImage=app.config['DEFAULT_IMAGE'], boardQueryData=boardQueryData)


@app.route("/entry", methods=["GET", "POST"])
def entry():
    """Page to view specific entries and option to download files"""
    if request.method == "GET":
        # DISPLAY AN ENTRY
        post_key = request.args.get('pk')
        try:
            entryQuery = """SELECT title, desc, tstp, mtl, nzl, support, note, stl_filename, img_filename, gcode_filename
                            FROM print_info S
                            WHERE post_key = ?
                            """
            entryQueryData = db.execute(entryQuery, post_key)
            entryData = entryQueryData[0]
            print('FETCHED DATA FROM DATABASE:')
            print(entryData)
            return render_template("entry.html", defaultImage=app.config['DEFAULT_IMAGE'], entryData=entryData)

        except:
            # UNABLE TO EXECUTE SQL QUERY
            return apology("Bad request", 400) 
    
    if request.method == "POST":
        try:
            # DOWNLOAD FILE FROM /ENTRY
            if request.form:
                media = request.form.get('download')
                extention = media.rsplit('.', 1)[1].lower()

                if extention == 'stl':
                    path = app.config['STL_UPLOADS']
                
                elif extention == 'gcode':
                    path = app.config['GCODE_UPLOADS']
                
                else:
                    return apology("Client request for files not allowed", 400)

            # SEND FILE {MEDIA} FROM {PATH} TO CLIENT AS ATTACHMENT
            print(f'{extention.upper()} FILE ---"{media}"--- BEING RETRIEVED')
            return send_from_directory(path, media, as_attachment=True)
        
        except:
            # UNABLE TO SEND FILE TO CLIENT FOR DOWNLOAD
            return apology("Client request bad", 400)
   
 
@app.route("/search", methods=["GET"])
def search():
    """Search other 3D printing sites for files"""

    return render_template("search.html")


@app.route("/about", methods=["GET", "POST"])
def about():
    """Tell about the website and offer some education resources"""

    return render_template("about.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    """Page to control content uploaded to website"""
    adminQuery = """SELECT title, desc, tstp, mtl, support, nzl, note, post_key, stl_filename, img_filename, gcode_filename 
                    FROM print_info
                    """
    if request.method == "GET":
        # EXECUTE SQL QUERY FOR ALL DATA FOR ADMIN VIEWING
        try: 
            adminQueryData = db.execute(adminQuery)
        
        except:
            # UNABLE TO EXECUTE SQL QUERY FOR ADMIN VIEWING
            print("UNABLE TO EXECUTE adminQuery")
            
        return render_template("admin.html", defaultImage=app.config["DEFAULT_IMAGE"], adminQueryData=adminQueryData)
        
    if request.method == "POST":
        if 'post_key' not in request.form:
            # UPLOAD ENTRY
            if request.form.get("title") == '' or request.form.get('desc') == '':
                return apology('Please fill out required text fields of the form', 400)

            # RETRIEVE FORM DATA AND GENERATE TIMESTAMP AND POST_KEY
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
                """Check 1) Data names are correct
                         2) STL filename is present and has .stl extention
                         3) File ext for each file is is valid
                    """
                for file in request.files:
                    filename = request.files[file].filename
                    inputName = request.files[file].name

                    # ENSURE STL FILE IS NOT ABSENT
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
                        # REDIRECT CLIENT IF NAME REQUESTED IS NOT RECOGNIZED
                        return redirect(url_for('admin'))

                    if filename != '':
                        if not accepted_extension(filename, ext):
                            return apology('Unsupported file type submitted', 400)
                        
                        else:
                            dict = {
                                'inputName': inputName, 
                                'filename': filename,
                                'column': column,
                                'requestObj': request.files[file],
                                'uploadPath': uploadPath
                                }
                            recieved_files.append(dict)
                    
                    # else:
                    #     # FILENAME SUBMITTED WAS BLANK
                    #     print(f"Filename is: [{filename}]")
                    #     return apology('Error saving file, please try again', 400)

            else:
                # NO FILES RECEIVED FROM CLIENT
                return apology('No files were submitted', 400)

            # SAVE FORM DATA
            print("SAVING FORM DATA ---------------------------------------->")
            try:
                # TRY TO INSERT RECEIVED DATA INTO DATABASE
                db.execute("INSERT INTO print_info (title, desc, tstp, mtl, support, nzl, note, post_key) \
                            VALUES(?, ?, ?, ?, ?, ?, ?, ?)", title, desc, tstp, mtl, support, nzl, note, post_key)
            
            except:
                # UNABLE TO INSERT RECEIVED DATA INTO DATABASE
                return apology('An error occured while saving form data to database', 400)

            # SAVE FILES TO STATIC/<DIRECTORY> & FILENAMES TO DATABASE
            print("SAVING FILES ---------------------------------------->")
            try:
                for fileDict in recieved_files:
                    print(f"SAVING -- '{fileDict['filename']}' -- TO FILE SYSTEM")
                    fileDict['requestObj'].save(os.path.join(fileDict['uploadPath'], fileDict['filename']))
                    
                    print(f"SAVING -- '{fileDict['filename']}' -- TO DATABASE")
                    db.execute(f"UPDATE print_info \
                                SET {fileDict['column']}='{fileDict['filename']}' \
                                WHERE post_key='{post_key}'")

                # REREQUERY FILES TO UPDATE ADMIN ENTRY TABLE
                adminQueryData = db.execute(adminQuery)
                return render_template('admin.html',  defaultImage=app.config["DEFAULT_IMAGE"], adminQueryData=adminQueryData)

            except: 
                # UNABLE TO SAVE FILE(S) TO DIR, DELETE DATA SAVED TO DATABASE FOR ENTRY
                adminQueryData = deleteAndRefresh(adminQuery, post_key)
                return apology('An error occured while saving files to database', 400)

        else:
            # DELETE ENTRY
            post_key = request.form.get("post_key")
            adminQueryData = deleteAndRefresh(adminQuery, post_key)
            return render_template("admin.html", defaultImage=app.config["DEFAULT_IMAGE"], adminQueryData=adminQueryData)


def deleteAndRefresh(argQuery, post_key):
    '''Delete entry and return updated data'''
    try:
        filenameQuery = f"""SELECT stl_filename, img_filename, gcode_filename 
                        FROM print_info 
                        WHERE post_key='{post_key}'
                        """
        filenameQueryData = db.execute(filenameQuery)
        filenames = list(filenameQueryData[0].values())
        
        # REMOVE FILE FROM PROJECT DIR IF FILENAME NOT IN DATABASE
        pathFilePair = tuple(zip(pathList, filenames))
        for item in pathFilePair:
            if item[1] != None:
                try:
                    print(f'Removing FILE {item[1]} from DIRECTORY {item[0]}')
                    path = os.path.join(item[0], item[1])
                    os.remove(path)

                except:
                    print(f"{item[1].upper()} NOT FOUND IN EXPECTED DIRECTORY")

        print(f'Removing ENTRY {post_key} from DATABASE')
        db.execute(f"DELETE \
                    FROM print_info \
                    WHERE post_key='{post_key}'")
        return db.execute(argQuery)
        
    except:
        # UNABLE TO REMOVE FILE(S) OR EXECUTE SQL QUERY 
        print(f"FAILED TO 1) DELETE FILE(S)  OR  2) DELETE DATA")
        return