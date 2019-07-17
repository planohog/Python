import datetime
import pifacedigitalio
from flask import Flask, render_template
gatered = 0
#bgcolor = ""
app = Flask(__name__)
@app.route("/")
def hello():
   
   pfd = pifacedigitalio.PiFaceDigital()
   gateclosed = pfd.input_pins[0].value
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   bgcolor ="white"
   if gateclosed == '1':
       bgcolor = 'green'

   if gateclosed == '0':
       bgcolor = 'red'

   templateData = {
      'title' : 'GATE',
      'time': timeString,
      'gate': gateclosed,
      'bcolor' : bgcolor
      }
   return render_template('test3.html', **templateData)


@app.route("/<deviceName>/<action>")
def action(deviceName, action):
    pfd = pifacedigitalio.PiFaceDigital()
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    gateclosed = pfd.input_pins[0].value

    if gateclosed == '1':
       bgcolor = 'green'  

    if gateclosed == '0':
       bgcolor = 'red'  

    if deviceName == 'gatechange':
          actuator = 1

    if action == "toggle":
     pfd.relays[0].value = 1 #
     from time import sleep
     sleep(1.1) # Time in seconds
     pfd.relays[0].value = 0 #
     #gateclosed = pfd.input_pins[0].value
   
    templateData = {
              'time'    : timeString,
              'gate'    : gateclosed,
              'bcolor'  : bgcolor
        }
    return render_template('test3.html', **templateData)


if __name__ == "__main__":
   app.run(host='0.0.0.0',  debug=True)
