#!/usr/bin/env python
 
import sys, os, time
import rrdtool
from datetime import datetime, timedelta
from socket import *
 
serverHost = 'cwop.aprs.net'
serverPort = 14580
address = 'YOURSTATIOIDHERE>APRS,TCPIP*:'
# Attention, format of the location is bit special. Although there is a dot, the values are in degrees, minutes and seconds!
position = 'DDMM.SSN/DDDMM.SSE_'
 
def send_packet():
    # Get the values from the database
    weather = rrdtool.fetch("./../weather_info/weather.rrd", 'AVERAGE', '-r 720', '-s -720')
    press = rrdtool.fetch("./../pressure_info/pressure.rrd", 'AVERAGE', '-r 600', '-s -600')
    # Attention, temperature in Fahrenheit!
    fahrenheit = 9.0/5.0 * weather[2][0][0] + 32
    humidity = weather[2][0][1]
    # Attention, barometric pressure in tenths of millibars/tenths of hPascal!
    pressure = press[2][0][1] * 10
 
    # If you have wind and rain data, get it here. Be aware that values are required in mph and in hundredths of an inch!
    wind_degrees = ...
    wind_mph = ...
    wind_gust_mph = ...
    precip_1hr_in = ...
    precip_today_in = ...
 
    # Prepare the data, which will be sent
    wx_data = make_aprs_wx(int(float(wind_degrees)),float(wind_mph),float(wind_gust_mph),fahrenheit,f_precip_1hr_in,None,(float(precip_today_in)*100),humidity,pressure)
    # Use UTC
    utc_datetime = datetime.now()
    # Create socket and connect to server
    sSock = socket(AF_INET, SOCK_STREAM)
    sSock.connect((serverHost, serverPort))
    # Log on
    sSock.send('user YOURSTATIOIDHERE pass -1 vers Python\n')
    # Send packet
    sSock.send(address + '@' + utc_datetime.strftime("%d%H%M") + 'z' + position + wx_data + 'Raspberry Pi\n')
    # Close socket, must be closed to avoid buffer overflow
    sSock.shutdown(0)
    sSock.close()
 
def make_aprs_wx(wind_dir=None, wind_speed=None, wind_gust=None, temperature=None, rain_last_hr=None, rain_last_24_hrs=None, rain_since_midnight=None, humidity=None, pressure=None):
    # Assemble the weather data of the APRS packet
    def str_or_dots(number, length):
        # If parameter is None, fill with dots, otherwise pad with zero
        if number is None:
            return '.'*length
        else:
            format_type = {
                'int': 'd',
                'float': '.0f',
            }[type(number).__name__]
            return ''.join(('%0',str(length),format_type)) % number
    return '%s/%sg%st%sr%sp%sP%sh%sb%s' % (
        str_or_dots(wind_dir, 3),
        str_or_dots(wind_speed, 3),
        str_or_dots(wind_gust, 3),
        str_or_dots(temperature, 3),
        str_or_dots(rain_last_hr, 3),
        str_or_dots(rain_last_24_hrs, 3),
        str_or_dots(rain_since_midnight, 3),
        str_or_dots(humidity, 2),
        str_or_dots(pressure, 5),
    )
 
try:
    send_packet()
except:
    sys.exit(-1)
