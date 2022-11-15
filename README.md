# 3D Print Anything Documentation
### Video Demo:  https://youtu.be/niYDRct1nQc
## Description
*3D Print Anything* (3DPA) is a 3D printing blog for uploading 3D prints (think small scale version of [Thingiverse](https://www.thingiverse.com/)).  Currently the project is only indended for personal use and not to be deployed.  The project's intent is to function as a view only blog users can browse content and download files, and the admin can post entries.  Entries are composed of an image, stl file, gcode file, various print information, and a 3D rending.  Perhaps in the future the project will be expanded to allow for deployment so that everyone can use it. 
## Tech
*3D Print Anything* was built using the following:
* [Flask](https://flask.palletsprojects.com/en/2.2.x/) - web framework
* Python3
* [Boostrap](https://getbootstrap.com/) - CSS framework
* HTML
* CSS
* [SQLite3](https://www.sqlite.org/index.html) - SQL database engine
* [Three.js](https://threejs.org/) - JavaScript library for 3D rendering
* JavaScript
## App Structure
The app was designed with the intention of a single user, the admin, uploading entries to be viewed by the general public.  Thus, the design of this app makes no attempt to handle large amounts of entries (150+).  The design uses lightweight frameworks like sqlite and flask for ease and simplicity. 

The database ```3d.db``` contains only one table, ```print_info```, which contains all print data for each print including filenames the image, stl file and gcode file, etc.  The ```print_info``` table also includes a ```post_key``` which is a 13 digit hex token assigned to each entry when uploaded as a way of identifying each entry.  The length of the ```post_key``` was chosen due to the statistical improbability of a key being generated that would match an existing key.  The hex token solution is quick and simple, but would be a poor choice for a project which requires scalability.

Each file uploaded as part of an entry is stored on the project path in a directory respective of the file's type (img, stl, gcode) within the ```/static``` directory.  Were this project to be deployed for public use, a better design for file storage would be Amazon S3 cloud storage. 

Admin controls are gain by loging in with admin credentials (username and password) on the ```/login``` page.  Once a login is successfull, the app will create a session to remember the admin is logged, during which the admin has upload and delete functionality.  When the loggout tab is clicked, the session is cleared and the user is redirected to the homepage once again without access to admin controls. 
## Configuration
The ```admin_config.py``` file holds a few global variables which the admin might want to configure:
* ```ADMIN_UN``` and ```ADMIN_PW``` set the admin username and password.
* ```SESSION_ID``` sets the session id used to keep the admin logged in.
* ```ALLOWED_IMAGE_EXTENSIONS``` is a python set of image file extentions that are allowed.
* db is the variable that holds the cursor to the sqlite database.  This can be toggled between a full database ```3d_full.db``` or and empty one ```3d.db```
* The rest are path configurations used to control upload destinations and the location of default media.

Cofigured in ```app.py```:
* Sessions are configured to use the project file system
* Each http request is configured not to be cashed

## Usage
To use the site as an admin the user must manually type into the url bar ```site-address/admin``` or ```site-address/login``` before being directed to the login page.  Once logged in using the admin username and password, an admin tab and a logout tab will apear on the right-hand side of the navigation bar allowing the admin to manage the contents of the site. Clicking on the logout tab will signout the admin and remove the admin tab and logout tab from the nav bar.

When uploading entries to the site:
* By default, only .stl, .gcode, .svg, .png, .jpg, and .jpeg files are submittable.  The app will handle any other file type submitted with a 400 error. 
* Entries must contain a title, description, and stl file. The app will handle vacant "required fields" with a 400 error, and the information will not be saved forcing the user to resubmit the form.
* Filenames must be unique with regard to other files of the same type on the site, otherwise the app will handle it with a 400 error (i.e. if a file called benchy.stl has been uploaded to the site already, the admin cannot upload another benchy.stl with another entry).
* An file submitted in the incorrect file field is handled as a 400 error (i.e. a png file submitted to the stl file field).
* If no image is uploaded, a default image will be used.

When searching the site for entries:
* The search query has minimum of 3 letters to search (i.e. searching "a" or "th" will not produce any results).
* The search query searches entry titles only (i.e. a queries for words in an entry description, or a filename are not guaranteed to produce any results).
## Running the app on your computer
To use the app, once all packages listed in requirements.txt have been installed, open the project folder in your IDE and enter the command ```flask run``` into the terminal to start the development server.  From there visit the link produced by the flask run command (which should be running the app on port 5000 unless otherwise configured). The link will take the user to the site homepage and from there the user may navigate to any of the three pages listed on nav bar or through the buttons within the homepage.
## App/Site Layout
The site content is managed by way of the Admin page, and all other pages are used to view and interact with that content.  All pages are responsive to various device widths (phone/computer/tablet).  The site pages are as follows: 
* **Home** (Nav bar title and logo) - Displays a short paragraph decsribing the inspiration for the project, some buttons linked to other pages, and a card deck containing 4 most recent entries uploaded. 
* **Board** - Displays all uploaded entries.  Each print entry is shown as card with a thumbnail image, a description, and a button which takes the user to that specific entry.
* **Entry** (for individual print) - Each entry page displays the image, title, description, datetime uploaded, print info, and a 3D interactive rendering of the stl file.  Both the stl file and the gcode file are available for download.
* **Search** - Contains 6 different search bars for finding 3D files.  The first search bar at the top of the screen is used to search *3DPA* for entries using titles.  The other 5 search bars below are linked to other website search queries, allowing the user to search for 3D files on other sites.
* **About** - The about page is a simple  introduction of the author (myself), the 3D printing tools I use and a button linked to the source code for the project.
* **Login** - A simple login page requiring username and password verification before allowing access to admin controls.
* **Admin** - The page used to control the content of the site.  Here the admin can upload or delete entries and view all content on the site.
## Features
Features of the site shown here are divided by two roles; admin and user. 
### Viewer features include:
* View recent entries (homepage)
* View all available entries
* View individual entries: print information including material, nozzle size, support required, etc.
* View stl files interactively (orbit controls are mouse for computer and fingers for touch screen)
* Download stl and gcode files
* Search site for entries by "title"
* Search other sites for 3D files (Thingiverse, Cults3D, Free3D, MyMiniFactory, Pinshape)

### Admin features include:
* All viewer feature plus...
* View all entries in a centralized table
* Upload an entry
* Delete entry

