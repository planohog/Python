########################## MAKE HASH ################################
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
flask_bcrypt = Bcrypt(app) # to prevent naming collisions.



@app.route("/")
def index():
    myhash ='$2b$12$M5OxY4lE7EN664o421VOIe/SyYtH82rj7ahr2OKiwfQ9yjlWd5FK.'
    password = '.2709.'
    pw_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')
    candidate = '.2709.'
    verifed_pass = flask_bcrypt.check_password_hash(myhash, candidate)

    if verifed_pass:
       return render_template('passhash.html', value=pw_hash)
    else:
       return render_template('failhash.html', value=pw_hash)



    return "[Hello World!]"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)
