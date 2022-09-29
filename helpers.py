from flask import render_template

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


def inputName_present():
    pass


def filename_present():
    pass


def accepted_extension(filename, ext):
    if isinstance(ext, str):
        return ("." in filename and filename.rsplit('.', 1)[1].lower() == ext)

    if isinstance(ext, set):
        return ("." in filename and filename.rsplit('.', 1)[1].lower() in ext)
    
    else:
        raise Exception('Unknown type')


def convertToBinary(filename):
    with open(f"/mnt/c/users/Ben Hogan/documents/CS 2022/CS50 - Harvard/Final Project Planning Files/{filename}", 'rb') as f:
        blob = f.read()
    return blob
