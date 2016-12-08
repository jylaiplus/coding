#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industries
# DHT22 data upload to ThingSpeak (DHT22 from Tony DiCola)

import sys
import Adafruit_DHT
import httplib, urllib
from time import localtime, strftime

#ThingSpeak API
def write_thingspeak(temperature, humidity):
        params = urllib.urlencode({'field1': temperature, 'field2': humidity, 'key':'TO9PYPW37OHTPFYR'})
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print response.status, response.reason
        data = response.read()
        conn.close()

# Parse command line parameters.
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
        sensor = sensor_args[sys.argv[1]]
        pin = sys.argv[2]
else:
        print 'usage: sudo ./Adafruit_DHT.py [11|22|2302] GPIOpin#'
        print 'example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO #4'
        sys.exit(1)

if humidity is not None and temperature is not None:
        print 'Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity)
        write_thingspeak(temperature, humidity)
else:
        print 'Failed to get reading. Try again!'
        sys.exit(1)
