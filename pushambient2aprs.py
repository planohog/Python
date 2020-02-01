import os
from socket import *
from datetime import datetime, time
import math

#below is not complete for os.env for security issues
os.environ["AMBIENT_ENDPOINT"] = 'https://api.ambientweather.net/v1'
os.environ["AMBIENT_API_KEY"] = 'c041469de789e55832b5b9461d91ca5d6a48b1b3eabb6aed74f7de'
os.environ["AMBIENT_APPLICATION_KEY"] = '363b808026833a7f8a1913dc12b9cb774d0b8342393e3bbf45b3'

from ambient_api.ambientapi import AmbientAPI

callsign = 'K'
latitude = XX.6911
longitude = XX.25722
devicename = 'WS2902' #This identifies your equipment/software. You can put anything you want. I use 'WS2902A', which is the model of weather station I have
#IMPORTANT: lat/long must be listed in DECIMAL DEGREES (DD.DDDD). Number of digits doesn't really matter. Use positive values for N/E, negative for S/W. The program then converts to degrees decimal minutes (DD MM.MMMM), which is the format APRS requires.

api = AmbientAPI()

devices = api.get_devices()
home = devices[0] #this assumes you have only one station. Increase number accordingly if you want to get data from others
weather= home.last_data

#convert coordinates to degrees decimal minutes
if latitude < 0:
    latitude = abs(latitude)
    latitude = str(int(latitude)).zfill(2) + str(round(60*(latitude - int(latitude)),2)).zfill(2) + 'S'
else:
    latitude = str(int(latitude)).zfill(2) + str(round(60*(latitude - int(latitude)),2)).zfill(2) + 'N'

if longitude < 0:
    longitude = abs(longitude)
    longitude = str(int(longitude)).zfill(3) + str(round(60*(longitude - int(longitude)),2)).zfill(2) + 'W'
else:
    longitude = str(int(longitude)).zfill(3) + str(round(60*(longitude - int(longitude)),2)).zfill(2) + 'E'

winddir = str(weather.get('winddir')).zfill(3)
windspeed = str(int(math.ceil(weather.get('windspeedmph')))).zfill(3)
windgust = str(int(math.ceil(weather.get('windgustmph')))).zfill(3)
if weather.get('tempf') < 0:
    temp = '-' + str(int(round(weather.get('tempf')))).zfill(2)
else:
    temp = str(int(round(weather.get('tempf')))).zfill(3)
rainhour = str(int(weather.get('hourlyrainin')*100)).zfill(3) #technically this is RATE of rain per hour, not AMOUNT per hour, but seems to be tolerated?
past24hoursrain = str(int(weather.get('dailyrainin')*100)).zfill(3) #at the moment, the Ambient API does not provide "rain in last hour", so no way to calculate "rain in last 24 hours." The API can only report "rain since local midnight." Therefore this only gets reported after 23:45 local time, so rain since midnight is reasonably close to rain in last 24 hours
dailyrain = str(int(weather.get('dailyrainin')*100)).zfill(3) #this value IS supposed to be "rain since local midnight," so it is always reported
pressure = str(int(weather.get('baromrelin')/0.0029529983071445)).zfill(5) #pressure is supposed to be reported to APRS in "altimiter" (QNH) format, that is, relative. The system itself corrects the pressure to sea level based on your station's listed elevation, so make sure that's accurate
humidity = str(int(weather.get('humidity')%100)).zfill(2) #uses modulus operator % so that 100% is given as '00'

# If luminosity is above 999 W/m^2, APRS wants a lowercase L
if weather.get('solarradiation') >= 1000:
	luminosity = 'l' + str(int(round(weather.get('solarradiation'))) % 1000).zfill(3)
else:
	luminosity = 'L' + str(int(round(weather.get('solarradiation')))).zfill(3)

# Time reported in Zulu (UTC). 24-hour rain workaround still has to be local time, though
packet = callsign + '>APRS,TCPIP*:@' + datetime.utcnow().strftime("%d%H%M") + 'z' + latitude + '/' + longitude + '_' + winddir + '/' + windspeed + 'g' + windgust + 't' + temp + 'r' + rainhour + 'p' + (past24hoursrain if datetime.now().time() >= time(23,45) else '...') + 'P' + dailyrain + 'h' + humidity + 'b' + pressure + luminosity + devicename

print(packet) #prints the assembled packet for debugging purposes

#send the packet
s = socket(AF_INET, SOCK_STREAM)
s.connect(('cwop.aprs.net', 14580))
s.send('user ' + callsign + ' pass -1 vers Python\n')
s.send(packet+'\n')
s.shutdown(0)
s.close()
