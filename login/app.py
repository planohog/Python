###########################################################
###########################################################
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_bcrypt import Bcrypt
import os
#
app = Flask(__name__)
flask_bcrypt = Bcrypt(app) # to prevent naming collisions.
###########################################################
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('opengate.html')
    else:
        return "Hello Boss!"
###########################################################
@app.route('/opengate', methods=['POST'])
def do_admin_login():
    myhash ='$2b$12$M5OxY4lE7EN664o421VOIe/SyYtH82rj7ahr2OKiwfQ9yjlWd5FK.'
    if  flask_bcrypt.check_password_hash(myhash, request.form['password'] ) and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()
###########################################################
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
###########################################################
# junk below this line                                    #

  #     return render_template('login.html')
  #@app.route('/login', methods=['POST'])
   # canidatepw = request.form['password']
   # verifed_pass = flask_bcrypt.check_password_hash(myhash, candidatepw)
   #    verifed_pass = flask_bcrypt.check_password_hash(myhash, request.form['password'] ) 
   #    if request.form['password'] == 'st0pspam' and request.form['username'] == 'admin':
   #    if verified_pass and request.form['username'] == 'admin':
#
#myhash ='$2b$12$M5OxY4lE7EN664o421VOIe/SyYtH82rj7ahr2OKiwfQ9yjlWd5FK.'
#    password = '.2709.'
#    pw_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')
#    candidate = '.2709.'
#    verifed_pass = flask_bcrypt.check_password_hash(myhash, candidate)
#
#    if verifed_pass:
#       return render_template('passhash.html', value=pw_hash)
#    else:
#       return render_template('failhash.html', value=pw_hash)
#
#
