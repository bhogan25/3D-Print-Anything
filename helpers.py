import os
from functools import reduce, wraps
from flask import render_template, session, redirect
from admin_config import SESSION_ID


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.
        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def accepted_extension(filename: str, ext: str) -> str:
    if isinstance(ext, str):
        return ("." in filename and filename.rsplit('.', 1)[1].lower() == ext)

    if isinstance(ext, set):
        return ("." in filename and filename.rsplit('.', 1)[1].lower() in ext)
    
    else:
        raise Exception('Unknown type')

def filenameTaken(filename: str, path: str) -> bool:
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    new_files = files.copy()
    new_files.append(filename)
    files = set(files)
    new_files = set(new_files)

    if reduce(lambda x, y : x and y, map(lambda p, q: p == q,list(files),list(new_files)), True):
        print("The lists are the same, duplicate found")
        return True
    else:
        print("The lists are not the same, file is not duplicate")
        return False

def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("admin_id") != SESSION_ID:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
