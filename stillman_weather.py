
 

#Almost all code came from http://bc-robotics.com/tutorials/raspberry-pi-weather-station-part-2/
import ascon
import encryption

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
from w1thermsensor import W1ThermSensor
 
import board
import busio
from adafruit_bme280 import basic as adafruit_bme280
i2c = busio.I2C(board.SCL, board.SDA)
 
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
 
import RPi.GPIO as GPIO
 
client = mqtt.Client(client_id = "Weather")
client.connect("96.66.89.56")

def sendText(raw_data, sensor_id, quality):
     client.publish(sensor_id, raw_data, qos = 0)

#bme = adafruit_bme280.Adafruit_BME280_I2C(i2c)
ads = ADS.ADS1015(i2c)
ads.gain = 1
 

ds18b20 = W1ThermSensor()
 
interval = 8   #How long we want to wait between loops (seconds)
windTick = 0   #Used to count the number of times the wind speed input is triggered
rainTick = 0   #Used to count the number of times the rain input is triggered
 
#Set GPIO pins to use BCM pin numbers
GPIO.setmode(GPIO.BCM)
 
#Set digital pin 17 to an input and enable the pullup 
 
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
 
#Set digital pin 23 to an input and enable the pullup 
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
 
#Event to detect wind (4 ticks per revolution)
GPIO.add_event_detect(17, GPIO.BOTH) 
def windtrig(self):
    global windTick
    windTick += 1
 
GPIO.add_event_callback(17, windtrig)
 
#Event to detect rainfall tick
GPIO.add_event_detect(23, GPIO.FALLING)
def raintrig(self):
    global rainTick
    rainTick += 1
 
GPIO.add_event_callback(23, raintrig)

count = 0

while count < 8:
 
    time.sleep(interval)
 
    #Pull Temperature from DS18B20
    temperature = ds18b20.get_temperature()
 

 
    #Pull pressure from BME280 Sensor & convert to kPa
 
    #Calculate wind direction based on ADC reading

 
    #Calculate average windspeed over the last 15 seconds
    windSpeed = (windTick * 1.2) / interval
    windTick = 0
 
    #Calculate accumulated rainfall over the last 15 seconds
    rainFall = rainTick * 0.2794
    inchRain = rainFall / 25.4
    rainTick = 0
    
    freedomSpeed = windSpeed * (312/500)
    freedomTemp = temperature * (9/5) + 32
    #Print the results
#     print( 'Temperature: ' , temperature)
#     print( 'Humidity:    ' , humidity, '%')
#     print( 'Pressure:    ' , pressure, 'kPa')
#     print( 'Wind Dir:    ' , windDir, ' (', windDeg, ')')
#     #print( 'Wind Speed:  ' , windSpeed, 'KPH')
#     print( 'Freedom Speed:  ' , freedomSpeed, 'MPH')
#     #print( 'Rainfall:    ' , rainFall, 'mm')
#     print( 'Rainfall in Inches:    ' , inchRain, 'inches')
#     print( ' ')
    
#     sendText((round(freedomTemp, 2)),"weather_temp", 0)
#     sendText((round(humidity, 2)),"weather_humidity", 0)
#     sendText(rainFall,"weather_rain", 0)
#     sendText(freedomSpeed,"weather_speed", 0)
#     sendText(windDir,"weather_wind", 0)
#     sendText(pressure,"weather_pressure", 0)

    message = ("22,weather,Major General (Ret.) Robert Morris Stillman's Field,"+str(round(freedomTemp, 2))
                  + "," + str(round(rainFall,2)) + "," + str(round(freedomSpeed,2)))    
    
#     message = "This is a test message that we are going to send to see what the difference in packet size is going to be. Hopefully this is going to be long enough that we should be able to see a difference. The first test I am conducting is a plaintext message" 
    
    message = "".join(map(str, message))
#     
        
    #
#     message = encryption.encrypt(message.encode())
    
    print(message) 
    
    sendText(message, "weather_", 0)         
    count = count + 1

raise SystemExit

