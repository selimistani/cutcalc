from flask import render_template

def apology(message, code=400):
    return render_template("apology.html", top=code, bottom=message), code
