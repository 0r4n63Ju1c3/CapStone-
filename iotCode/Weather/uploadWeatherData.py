# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 11:00:50 2021

@author: C22Turner.Nims

The purpose of this file is to parse data sent over mqtt and publish it to the database
"""

import paho.mqtt.client as mqtt
import time, random
from datetime import datetime
import math
import sys
sys.path.append("/home/pi/Desktop/IOT_Capstone/Code/iot_capstone22/")
import iot_lib
import iotComm as comm
import encryption
import json

client_name = "weatherPi1"
server_ip = "96.66.89.56" #public ip address of mqtt server
#channel_name = "weather_all"
channel_name = "weather_cybercity"



def getImagePath(temp, rain, wind):
    if wind > 16:
        return "images/einkimages/too_windy.png"
    elif temp < 32:
        return "images/einkimages/too_cold.png"
    elif temp > 90:
        return "images/einkimages/too_hot.png"
    elif rain > 0:
        return "images/einkimages/rainy.png"
    else:
        return "images/einkimages/good_to_fly.png"

#this is what to do when a message is sent on the mqtt channel
def on_message(client, userdata, message):

    binary_data = message.payload #read data as string
    data = encryption.decrypt(bytes(binary_data)).decode()
    #print(data)
    #parse data

    #create dictionary of data
    weather_dictionary = json.loads(data)
    print(weather_dictionary)


    device_id = weather_dictionary["data_type"] + weather_dictionary["sensor_ID"] #assuming we want to clientname to be the deviceid in the database

    #upload to weather database
    print("Data upload")
    response = iot_lib.upload_data(weather_dictionary, device_id, api_key=12345)
    print(response)

    temp = float(weather_dictionary["temperature"])
    rainfall = float(weather_dictionary["rainfall"])
    windspeed = float(weather_dictionary["windspeed"])

    #update e-ink information in database
    message = "Temp: " + str(temp) + " degrees F\n" + "Wind Speed: " + str(windspeed) + " mph\n" + "Current rainfall: " + str(rainfall) + " inches\n"


    #create dictionary of data
    eInk_dictionary = {
      "faculty_name": "Weather Report",
      "title":datetime.now().strftime("%B %d, %Y   %H:%M:%S"),
      "message":message,
      "location":weather_dictionary["location"],
      "file_path":getImagePath(temp, rainfall, windspeed)
}

    print("Data update")
    print(message)
#   update_data(data_dictionary, device_id, api_key=12345, table_name, row_id, time):
    response = iot_lib.update_data(eInk_dictionary, device_id, 12345, "eink_messages", 1)

    print(response)

def on_connect(client, userdata, flags, rc):
    print("Connected. Subscribing to:", CHANNELS)
    client.subscribe(CHANNELS)

#MAIN
#listen on mqtt
CHANNELS = [ (channel_name, 0), ]
print("Connecting to MQTT Server...")
comm.client.on_connect = on_connect
comm.client.on_message = on_message

while (True):
    try:
        comm.client.connect(comm.MQTT_SERVER_IP)
        start_time = time.time()
        print("Listening for messages on:", CHANNELS)
        comm.client.loop_forever()
    except Exception as e:
        print("Connection failed after " + str(time.time()-start_time) + " seconds.")
        print(e)
        time.sleep(10)
    comm.client.disconnect()
    comm.client.loop_stop()
