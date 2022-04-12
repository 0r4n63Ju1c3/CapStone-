"""
MQTT Light Demo
Author:  Lt Col Adrian A. de Freitas
Description:  Shows an example of how to control nanoleaf
              lights using MQTT messages
              
              Nanoleaf API is available at:
              https://nanoleafapi.readthedocs.io/en/latest/
"""

#Required Imports
from nanoleafapi import Nanoleaf, NanoleafDigitalTwin
import paho.mqtt.client as mqtt
import datetime, time, random
import math
import encryption
import sys
import socket
import json
import requests

    
#This is where you enter the IP address of the lights
#nanoleaf_all = Nanoleaf("192.168.1.123")

#Below object gets the information for the lights and sets them up to be individually controlled
#nanoleaf_single = NanoleafDigitalTwin(nanoleaf_all)

#Gets light arrays from left to right and then prints the port values of them
#lights = nanoleaf_single.get_ids()
#print(lights)

#Light Processing for UOD, Random, and Graduating Class Year
start = datetime.datetime.now()
other = datetime.datetime.today().weekday()
startMin = start.minute
stop = 0
day = start.day
#print(day)
random.seed()
now = datetime.datetime.now()
minutes = abs(now.minute - startMin)

#Light IDs
#51239, 51544, 38038, 996, 23186, 48848, 2877, 6038, 64470, 30088, 39253, 43520, 23197, 9483, 64089, 0
#62926, 18230, 6487, 36139, 59658, 42639, 50977, 51324, 60486, 5499, 0


ip = socket.gethostbyname(socket.gethostname() +".local")
print(ip)

def on_message(client, userdata, message):
    """ Event Handler for when this program gets an MQTT Message.
        NOTE:  All subscribed topics are processed here

    Parameters
        ----------
        client
            The MQTT Client object
        userdata
            Information about the user
        message
            The message received from the MQTT broker
    """
    print("------------------------------------")
    print("MQTT Message Received at", datetime.datetime.now())
    print("Topic=",message.topic)
    print("qos=",message.qos)
   # print("message=", str(message.payload.decode("utf-8")))
    print("------------------------------------")
    
    now = datetime.datetime.now()
    minutes = abs(now.minute - startMin)
    message = message.payload
    print(message)
    #message = (encryption.decrypt(message))
    data_dict = json.loads(message)
    sender_id = data_dict["sender_id"]

    
#Json Message, loading data from weather station and preparing to process/send useful data to lights
    weather_dict = json.loads(data_dict["data"])
    sender_location = data_dict["location"]
    sender_time = data_dict["time"]
    sender_temp = float(weather_dict["temperature"])
    sender_windspeed = float(weather_dict["windspeed"])
    sender_rainfall = float(weather_dict["rainfall"])
    message = {}
    
#RAIN Light Control
    if sender_rainfall <= 0.2:
        message = {"array":"*", "light":0, "r":0, "g":255, "b":0}
        message = json.dumps(message)
        client.publish("lights", message, 0)
    else:
        message = {"array":"*", "light":0, "r":255, "g":0, "b":0}
        message = json.dumps(message)
        client.publish("lights", message, 0)

#Wind Speed Light Control
    if sender_windspeed <= 4:
        message = {"array":"*", "light":1, "r":0, "g":255, "b":0}
        message = json.dumps(message)
        client.publish("lights", message, 0)
    else:
        message = {"array":"*", "light":1, "r":255, "g":0, "b":0}
        message = json.dumps(message)
        client.publish("lights", message, 0)
             
#Temperature Light Control
    if 40 <= sender_temp <= 80:
        message = {"array":"*", "light":2, "r":0, "g":255, "b":0}
        message = json.dumps(message)
        client.publish("lights", message, 0)
    else :
        message = {"array":"*", "light":2, "r":255, "g":0, "b":0}
        message = json.dumps(message)
        client.publish("lights", message, 0)

#Random Light Control
    R = random.randint(50,200)
    G = random.randint(50,200)
    B = random.randint(50,200)
    message = {"array":"*", "light":3, "r":R, "g":G, "b":B}
    message = json.dumps(message)
    client.publish("lights", message, 0)

#Year Light Control
    year = now.year
    month = now.month
    if month > 5:
        year = year + 1
    print(year)
    if year % 4 == 0:
        message = {"array":"*", "light":4, "r":0, "g":0, "b":250}
        message = json.dumps(message)
        client.publish("lights", message, 0)
    elif year % 4 == 1:
        message = {"array":"*", "light":4, "r":110, "g":110, "b":110}
        message = json.dumps(message)
        client.publish("lights", message, 0)
    elif year % 4 == 2:
        message = {"array":"*", "light":4, "r":250, "g":0, "b":0}
        message = json.dumps(message)
        client.publish("lights", message, 0)
    elif year % 4 == 3:
        message = {"array":"*", "light":4, "r":200, "g":175, "b":55}
        message = json.dumps(message)
        client.publish("lights", message, 0)
        
#Period Light Control
    if (now.hour == 7 and now.minute >= 30):
        period = 1
        message = {"array":"*", "light":5, "r":255, "g":0, "b":0}
        message = json.dumps(message)
        client.publish("lights", message, 0)
    elif (now.hour == 8 and now.minute <= 23):
        period = 1
        message = {"array":"*", "light":5, "r":255, "g":0, "b":0}
        message = json.dumps(message)
        client.publish("lights", message, 0)
    elif (now.hour == 8 and now.minute >= 30):
        period = 2
        message = {"array":"*", "light":5, "r":255, "g":127, "b":0}
        message = json.dumps(message)
        client.publish("lights", message, 0)
    elif (now.hour == 9 and now.minute <= 23):
        period = 2
        message = {"array":"*", "light":5, "r":255, "g":127, "b":0}
        message = json.dumps(message)
        client.publish("lights", message, 0)
    elif (now.hour == 9 and now.minute >= 30):
        period = 3
        message = {"array":"*", "light":5, "r":255, "g":255, "b":0}
        message = json.dumps(message)
        client.publish("lights", message, 0)
    elif (now.hour == 10 and now.minute <= 23):
        period = 3
        message = {"array":"*", "light":5, "r":255, "g":255, "b":0}
        message = json.dumps(message)
        client.publish("lights", message, 0)
    elif (now.hour == 10 and now.minute >= 30):
        period = 4
        message = {"array":"*", "light":5, "r":0, "g":255, "b":0}
        message = json.dumps(message)
        client.publish("lights", message, 0)
    elif (now.hour == 11 and now.minute <= 23):
        period = 4
        message = {"array":"*", "light":5, "r":0, "g":255, "b":0}
        message = json.dumps(message)
        client.publish("lights", message, 0)
    elif (now.hour == 12 and now.minute >= 45):
        period = 5
        message = {"array":"*", "light":5, "r":0, "g":0, "b":255}
        message = json.dumps(message)
        client.publish("lights", message, 0)
    elif (now.hour == 13 and now.minute <= 38):
        period = 5
        message = {"array":"*", "light":5, "r":0, "g":0, "b":255}
        message = json.dumps(message)
        client.publish("lights", message, 0)
    elif (now.hour == 13 and now.minute >= 45):
        period = 6
        message = {"array":"*", "light":5, "r":75, "g":0, "b":130}
        message = json.dumps(message)
        client.publish("lights", message, 0)
    elif (now.hour == 14 and now.minute <= 38):
        period = 6
        message = {"array":"*", "light":5, "r":75, "g":0, "b":130}
        message = json.dumps(message)
        client.publish("lights", message, 0)
    elif (now.hour == 14 and now.minute >= 45):
        period = 7
        message = {"array":"*", "light":5, "r":148, "g":0, "b":211}
        message = json.dumps(message)
        client.publish("lights", message, 0)
    elif (now.hour == 15 and now.minute <= 38):
        period = 7
        message = {"array":"*", "light":5, "r":148, "g":0, "b":211}
        message = json.dumps(message)
        client.publish("lights", message, 0)
    else:
        period = 0
        message = {"array":"*", "light":5, "r":200, "g":200, "b":200}
        message = json.dumps(message)
        client.publish("lights", message, 0)
        
#UOD Light Control
    if (other == 0) or (other == 1) or (other == 3) :
        message = {"array":"*", "light":6, "r":60, "g":100, "b":240}
        message = json.dumps(message)
        client.publish("lights", message, 0)
    elif other == 4 :
        message = {"array":"*", "light":6, "r":10, "g":150, "b":10}
        message = json.dumps(message)
        client.publish("lights", message, 0)
    else :
        message = {"array":"*", "light":6, "r":80, "g":52, "b":26}
        message = json.dumps(message)
        client.publish("lights", message, 0)
        


def is_connected_to_internet():
    url = "http://www.google.com"
    timeout = 5
    try:
        request = requests.get(url, timeout=timeout)
        print("Connected to Internet")
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No Internet Connection")
        return False
   
# Tells the client what function to call when a message
# is received

# Perpetually Listens for Messages on Subscribed Topics
while (not is_connected_to_internet()):
        time.sleep(5.0)
        
print("Listening to MQTT server...")
client = mqtt.Client()

# Connects to the MQTT Broker
client.connect("96.66.89.56")

# Subscribes to a Topic to Receive Messages
client.subscribe("weather_all", qos=0)

client.on_message = on_message



client.loop_forever()

    
    

        


