#################################################################
#################################################################
# Python3 pifacedigital2 automatic gate opener 
# requires external routing to get external IP  
# raspberian buster  pi2 
# July 16 2019 
# tmoore KG5TJT https://github.com/planohog/Python
#################################################################
#################################################################
import datetime
import pifacedigitalio
from flask import Flask, render_template
app = Flask(__name__)
@app.route("/")
def hello():
   pfd = pifacedigitalio.PiFaceDigital()
   gateclosed = pfd.input_pins[0].value
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   backcolor ="white"
   if gateclosed == 1 :
       backcolor = 'green'

   if gateclosed == 0 :
       backcolor = 'red'

   templateData = {
      'title' : 'GATE',
      'time': timeString,
      'gate': gateclosed,
      'bgcolor' : backcolor
      }
   return render_template('gate.html', **templateData)
#################################################################
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
    backcolor ="white"
    pfd = pifacedigitalio.PiFaceDigital()
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    gateclosed = pfd.input_pins[0].value
    if gateclosed == 1 :
       backcolor = 'green'  

    if gateclosed == 0 :
       backcolor = 'red'  

    if deviceName == 'gatechange':
       actuator = 1

    if action == "toggle" and actuator == 1:
     pfd.relays[0].value = 1 #
     from time import sleep
     sleep(1.1) # Time in seconds
     pfd.relays[0].value = 0 #
   
    templateData = {
              'time'    : timeString,
              'gate'    : gateclosed,
              'bgcolor' : backcolor
        }
    return render_template('gate.html', **templateData)
#################################################################
if __name__ == "__main__":
   app.run(host='0.0.0.0',port=2709,debug=True)
#################################################################
