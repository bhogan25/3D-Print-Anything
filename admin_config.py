import os
from werkzeug.security import generate_password_hash
from cs50 import SQL

# Configure Admin username, password, session id and initial session value
ADMIN_UN = "ADMIN"
ADMIN_PW = generate_password_hash("0.123456789")
SESSION_ID = "adm"

# Establish allowed img extentions
ALLOWED_IMAGE_EXTENSIONS = {'svg', 'png', 'jpg', 'jpeg'}

# Configure SQLite database
db = SQL("sqlite:///3d_full.db")

# Configure Upload Paths
MAIN_PATH = str(os.getcwd())
STL_UPLOADS = MAIN_PATH + "/static/stl"
IMAGE_UPLOADS = MAIN_PATH + "/static/img"
GCODE_UPLOADS = MAIN_PATH + "/static/gcode"
pathList = [STL_UPLOADS, IMAGE_UPLOADS, GCODE_UPLOADS]
DEFAULT_IMAGE = "static/0perm-media/default-no-image.png"