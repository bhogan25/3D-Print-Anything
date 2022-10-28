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


def accepted_extension(filename, ext):
    if isinstance(ext, str):
        return ("." in filename and filename.rsplit('.', 1)[1].lower() == ext)

    if isinstance(ext, set):
        return ("." in filename and filename.rsplit('.', 1)[1].lower() in ext)
    
    else:
        raise Exception('Unknown type')
