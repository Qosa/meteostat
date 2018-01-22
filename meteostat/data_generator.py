import sys
import os
import math
from datetime import datetime
from soundlevel_sensor import soundmeter
from light_sensor import photolux
sys.path.insert(0, '/home/pi/Desktop/meteostation/Adafruit_Python_DHT/examples/')
from dht11 import dht11
sys.path.insert(0,'/home/pi/Desktop/meteostation/Adafruit-Raspberry-Pi-Python-Code/Adafruit_Python_BMP/examples')
from simpletest import bmp180


def getSensorData(df):
    data = {}
    noiseSensor = "{0:.2f}".format(20*math.log10(float(soundmeter())/0.775))
    lightSensor = photolux()
    tempHumSensor = dht11()
    pressureSensor = bmp180()
    data["temp"] = (float(str(tempHumSensor[0]))+float(pressureSensor[0]))/2
    data["humidity"] = tempHumSensor[1]
    data["noise"] = noiseSensor
    data["lux"] = lightSensor
    data["temp2"] = pressureSensor[0]
    data["pressure"] = pressureSensor[1]
    data["altitude"] = pressureSensor[2]
    data["slp"] = pressureSensor[3]
    df = df.append({'Temperature':  data["temp"],'Humidity' : data["humidity"], 'Pressure': data["pressure"], 'Sea_level_pressure': data["slp"], 'Altitude': data["altitude"], 'Noise_level': data["noise"], 'Light_intensity': data["lux"], 'Time': datetime.now().strftime("%H:%M:%S")}, ignore_index = True)
    if not os.path.isfile('meteo.csv'):
        df.to_csv('meteo.csv')
    else:
        df.to_csv('meteo.csv',mode = 'a',header=False)
    return data, df