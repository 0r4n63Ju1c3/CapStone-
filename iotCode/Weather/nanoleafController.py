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


# CONSTANTS
# TODO:  Use the comm library instead!
BROKER_IP = "96.66.89.56"
LIGHT_COMMAND_CHANNEL = "lights"


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
    print("------------------------------------")
    
    message = message.payload        
    configure_lights(message)


def configure_lights(message):
    global lights
    print("Configuring Lights with", str(message))
    data_dict = json.loads(message)
    
    if data_dict['array'] == LIGHT_ID or data_dict['array'] == "*":
            i = int(data_dict['light'])
            r = int(data_dict['r'])
            g = int(data_dict['g'])
            b = int(data_dict['b'])
            nanoleaf_single.set_color(lights[i], (r, g, b))
            nanoleaf_single.sync()


# ----------------------------------------------
# Main client program
# ----------------------------------------------

# Ask Questions from the User
LIGHT_ID = int(input("Light ID: "))
NANOLEAF_IP = input("IP Address: ") #"192.168.1.123"

#This is where you enter the IP address of the lights
print("Connecting to Nanoleaf Array at", NANOLEAF_IP)
nanoleaf_all = Nanoleaf(NANOLEAF_IP)

#Below object gets the information for the lights and sets them up to be individually controlled
nanoleaf_single = NanoleafDigitalTwin(nanoleaf_all)

#Gets light arrays from left to right and then prints the port values of them
lights = nanoleaf_single.get_ids()
print("Light IDs:", lights)

# Configures the MQTT Client
client = mqtt.Client()
client.on_message = on_message

# Connects to the MQTT Broker
print("Attempting to Connect to MQTT")
client.connect(BROKER_IP)
print("SUCCESS!")

# Subscribes to the correct channel(s)
client.subscribe(LIGHT_COMMAND_CHANNEL, qos=0)

# Perpetually Listens for Messages on Subscribed Topics
client.loop_forever()
