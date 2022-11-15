# 3D Print Anything Documentation
## Video Demo:  <URL HERE>
## Description
*3D Print Anything* (3DPA) is Flask based web application for uploading 3D prints (think small scale version of [Thingiverse](https://www.thingiverse.com/)), currently for personal use only and is not deployed.  The project's original intent was to function as a blog where the admin could post entries composed of an image, a stl file, a gcode file, various print information, and a 3D rending of the file to be viewed by the public. However, due to time constraints, the application is only designed to be used locally and the role of user and admin are not distinguished.  Perhaps in the future the project will be expanded to fulfil its original purpose. 
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
The app was designed with the intention of a single user, the admin, uploading entries composed of an image, 3D stl file, gcode, and general print information to be viewed by a user (the public).  Thus, the design of this app makes no attempt to handle large amounts of entries (150+).  The design is uses lightweight frameworks like sqlite and flask for simplicity. 

The database ```3d.db``` contains only one table, ```print_info```, which contains all print data for each print including filenames the image, stl file and gcode file, etc.  The ```print_info``` table also includes a ```post_key``` which is a 13 digit hex token assigned to each entry when uploaded as a way of identifying each entry.  The length of the ```post_key``` was chosen due to the statistical improbability of a key being generated that would match an existing key.  This solution is simplistic and avoiding a "counter" system to assign a unique identifier but would be a poor choice for a project which requires scalability.  

Each file uploaded with an entry is stored in a directory respective of the file's type (img, stl, gcode) within the ```/static``` directory.  Where this project to be deployed for public use, an option for a better design for file storage would be Amazon S3 cloud storage. 

The app is not configured to use sessions and is specifically configured not to server responses.

## Usage
When uploading entries to the site:
* Only .stl, .gcode, .svg, .png, .jpg, and .jpeg files are submittable.  The app will handle any other file type submitted with a 400 error. 
* Entries must contain a title, description, and stl file. The app will handle vacant "required fields" with a 400 error.  The information will not be saved and the user will have to resubmit the form.
* Filenames must be unique with regard to other files of the same type on the site, otherwise the app will handle it with a 400 error (i.e. if a file called benchy.stl has been uploaded to the site already, the admin cannot upload another benchy.stl with another entry).
* An file submitted in the incorrect file field is handled as a 400 error (i.e. a png file submitted to the stl file field).
* If no image is uploaded, a default image will be used.

When searching the site for entries:
* The search query has minimum of 3 letters to search (i.e. searching "a" or "th" will not produce any results).
* The search query searches entry titles only (i.e. a query for words in an entry description, or a filename is not guaranteed to produce any results).


## Running the app on your computer
To use the app, once all packages listed in requirements.txt have been installed using python package installer ```pip3 install <module>```, open the project folder in your IDE and enter ```flask run``` to start the development server.  From there visit the link produced by the flask run command (which should be running the app on port 5000 unless otherwise configured). The link will take the user to the site homepage and from there the user may navigate to any of the three pages listed on nav bar or through the buttons within the homepage.
## App/Site Layout
The site contents are managed by way of the Admin page, and all other pages are used to view and interact with those contents.  Each page is responsive and various device widths (phone/computer/tablet).  The site pages are as follows: 
* **Home** (Nav bar title and logo) - Displays a short paragraph decsribing the inspiration for the project, some buttons linked to other pages, and a card deck containing 4 most recent entries uploaded. 
* **Board** - Displays all uploaded entries.  Each print entry is shown as card that shows a thumbnail image of the 3D file (if uploaded by the user), a description, and a button which takes the user to that specific entry. 
* **Entry** (for individual print) - Each entry page displays the image, title, description, datetime uploaded, print info, and a 3D interactive rendering of the stl file.  Both the stl file and the gcode file are available for download.
* **Search** - Contains 6 different search bars for finding 3D print files.  The first search bar at the top of the screen is used to search *3DPA* for entries using titles.  The other 5 search bars below are linked to other website search queries, allowing the user to search for 3D files on other sites.
* **About** - The about page is a simple  introduction of the author (myself), the 3D printing tools I use and a button linked to the source code for the project.
* **Admin** - The page used to control the contents of the site.  Here the admin can upload, delete and view all entries in the on the site.
## Features
Since the project was initially designed to be used as a blog to be viewed by *viewers* and to be managed by an *admin*, the feature explanations will be divided by those two roles. 
### User
The user features include: 
* View recent entries (homepage)
* View all available entries
* View individual entries: print information including material, nozzle size, support required, etc.
* View stl files interactively (orbit controls are mouse for computer and fingers for touch screen)
* Download stl and gcode files
* Search site for entries by "title"
* Search other sites for 3D files (Thingiverse, Cults3D, Free3D, MyMiniFactory, Pinshape)

### Admin
* View all entries and contents in a centralized table
* Upload an entry
* Delete entry

