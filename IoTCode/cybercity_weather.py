
#Almost all code came from http://bc-robotics.com/tutorials/raspberry-pi-weather-station-part-2/
import ascon
import encryption

import paho.mqtt.client as mqtt

import time

#from adafruit_bme280 import basic as adafruit_bme280

import json
import mqtt_protocol
import iotComm as comm


#
# def sendText(raw_data, sensor_id, quality):
#      client.publish(sensor_id, raw_data, qos = 0)

def on_connect(client, userdata, flags, rc):
    print("Connected. Subscribing to channels:", CHANNELS)
    print()

comm.client.on_connect = on_connect
print("Connecting to MQTT Server...")
comm.client.connect(comm.MQTT_SERVER_IP)

interval = 10   #How long we want to wait between loops (seconds)
runMinutes = 58 #Use this to set how long the code will run
stopValue = ((runMinutes * 60)/interval) #This gets how many times through the send loop the code will run
stopValue = 5

count = 0

while count < stopValue:

    temperature = 71

    #Calculate average windspeed over the last 15 seconds
    windSpeed = 71

    #Calculate accumulated rainfall over the last 15 seconds
    rainFall = 71
    inchRain = 71

    freedomSpeed = 71
    freedomTemp = 4


    weatherData = {
                   'temperature': str(round(freedomTemp, 2)),
                   'rainfall': str(round(rainFall,2)),
                   'windspeed': str(round(freedomSpeed,2))}
                   
                   
    data_str = json.dumps(weatherData)
    
    #data_str = "hello world"

    #pi_id = "weather1"
    #pi_location = "Major Birrer's Cyber City"
    
    pi_id = "weather1"
    pi_location = "Andrew Lee's laptop"
    
    print(data_str)

    comm.send("weather_encrypt", pi_id, pi_location, "weather_listener", data_str)
    print("sent")

    count = count + 1
    time.sleep(interval)

raise SystemExit
