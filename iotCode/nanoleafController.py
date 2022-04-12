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
#import encryption
import sys
import socket
import json
import time
import requests


# CONSTANTS
# TODO:  Use the comm library instead!
BROKER_IP = "96.66.89.56"
LIGHT_COMMAND_CHANNEL = "lights"


# ----------------------------------------------
# Verifies Internet Connection
# Returns True or False
# ----------------------------------------------
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


# ----------------------------------------------
# MQTT Event Handler
# Called on MQTT Connect/Reconnect
# ----------------------------------------------
def on_connect(client, userdata, flags, rc):
        print("MQTT Connection Detected")
        
        # Subscribes to the correct channel(s)
        client.subscribe(LIGHT_COMMAND_CHANNEL, qos=1)


# ----------------------------------------------
# MQTT Event Handler
# Called when MQTT Message Received
# ----------------------------------------------
def on_message(client, userdata, message):
    print("------------------------------------")
    print("MQTT Message Received at", datetime.datetime.now())
    print("Topic=",message.topic)
    print("qos=",message.qos)
    print("------------------------------------")
    
    message = message.payload        
    configure_lights(message)


# ----------------------------------------------
# NANOLEAF Function
# Converts a JSON Message to Nanoleaf Commands
# ----------------------------------------------
def configure_lights(message):
    global lights
    print("Configuring Lights with", str(message))
    
    debug_message = { "array":LIGHT_ID }

    try:
        data_dict = json.loads(message)
        
        # Attempts to Configure Lights Set for this Array
        if data_dict['array'] == LIGHT_ID or data_dict['array'] == "*":
                r = int(data_dict['r'])
                g = int(data_dict['g'])
                b = int(data_dict['b'])
                
                if data_dict['light'] != '*':
                    # Controlling an Individual Light
                    i = int(data_dict['light'])
                    nanoleaf_single.set_color(lights[i], (r, g, b))
                else:
                    # Controlling all Lights in the Array
                    for i in range(len(lights)):
                        nanoleaf_single.set_color(lights[i], (r, g, b))

                # Transmits the command
                nanoleaf_single.sync()

                debug_message['message'] = "Received request to configure light  " + str(data_dict['light']) + " to R: " + str(r) + " G: " + str(g) + " B: " + str(b)
    
    except Exception as e:
        print("Problem Occurred Processing Message")
        print("Error:", str(e))
        debug_message['message'] = "ERROR: " + str(e)

    # Transmits a Debug Message
    client.publish(topic="debug", payload=json.dumps(debug_message), qos=0)


# ----------------------------------------------
# Main client program
# ----------------------------------------------

try:
    # Get Light ID
    if len(sys.argv) >= 3:
        # Use Command Line Arguments
        LIGHT_ID = int(sys.argv[1])
        NANOLEAF_IP = sys.argv[2]
        print("LIGHT_ID:", LIGHT_ID)
        print("NANOLEAF_IP:", NANOLEAF_IP)
    else:
        # Ask Questions from the User
        LIGHT_ID = int(input("Light ID: "))
        NANOLEAF_IP = input("IP Address: ") #"192.168.1.123"

    while (not is_connected_to_internet()):
        time.sleep(5.0)

    #This is where you enter the IP address of the lights
    print("Connecting to Nanoleaf Array at", NANOLEAF_IP)
    nanoleaf_all = Nanoleaf(NANOLEAF_IP)

    #Below object gets the information for the lights and sets them up to be individually controlled
    nanoleaf_single = NanoleafDigitalTwin(nanoleaf_all)

    #Gets light arrays from left to right and then prints the port values of them
    lights = nanoleaf_single.get_ids()
    print("Light IDs:", lights)

    # Configures the MQTT Client
    client = mqtt.Client(client_id="lights_" + str(LIGHT_ID), clean_session=False)
    client.on_message = on_message
    client.on_connect = on_connect

    # Connects to the MQTT Broker
    print("Attempting to Connect to MQTT")
    client.connect(BROKER_IP)
    print("SUCCESS!")

    # Perpetually Listens for Messages on Subscribed Topics
    client.loop_forever()

except Exception as e:
    print("Exception Encountered:", e)
    client.publish(topic="debug", payload="Light Controller Failed: " + str(e), qos=0)
    