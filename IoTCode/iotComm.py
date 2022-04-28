# -------------------------------------------
# Communication Library
# -------------------------------------------
import paho.mqtt.client as mqtt
import socket
import os
import json
import subprocess
import encryption
from datetime import datetime

DEBUG = False
MQTT_SERVER_IP = "96.66.89.56"
C2_ID = "eInk_Pi0000000" #Pi id of the C2 pi


# ----------------------------------------
# Returns a iot protocol formated string
# ----------------------------------------
def wrapMessage(sender_id, pi_location, receiver_id, data):

    try:
        #get wifi network
        ssid = 'GREENNE2-CYBERCITY'
        #print(ssid)
    except Exception as e:
        #print(e)
        ssid = "Undefined: " + e
        
    try:
        #get ip
        ip = '127.0.0.1'
        #print(ip)
    except Exception as e:
        #print(e)
        ip = "Undefined: " + e
        
    #get time
    time = datetime.now().strftime("%B %d, %Y   %H:%M:%S")
    #print(time)
    
    dictionary = {
        "sender_id": sender_id,
        "location": pi_location,
        "ssid": ssid,
        "ip": ip,
        "time": time,
        "receiver_id": receiver_id,
        "data": data
        }
    #print(dictionary)
    return json.dumps(dictionary)

# ----------------------------------------
# Returns the name of the computer
# ----------------------------------------
def getHostname():
    return socket.gethostname()

# ----------------------------------------
# Event Handler when Connected
# ----------------------------------------
def on_connect(client, userdata, flags, rc):
    if DEBUG:
        print("CONNECT:", client, userdata, flags, rc, "\n")


# ----------------------------------------
# Event Handler when Disconnected
# ----------------------------------------
def on_disconnect(client, userdata, rc):
    if DEBUG:
        print("DISCONNECT:", client, userdata, rc, "\n")


# ----------------------------------------
# Connects the client to the broker
# ----------------------------------------
def connect(destination):
    client.connect(destination)


# ----------------------------------------
# Sends a message on a channel
# Assumes you are connected
# ----------------------------------------
def send(channel, sender_id, sender_location, receiver_id, message):
    if DEBUG:
        print("Sending message:")
        print("  Channel:", channel)
        print("  Message:", message, "\n")
    
    #client.publish(channel, encode(wrapMessage(sender_id, sender_location, receiver_id, message)))
    client.publish(channel, encryption.encrypt(encode(wrapMessage(sender_id, sender_location, receiver_id, message)).encode()))
    
    
    
# ----------------------------------------
# Disconnects from the broker
# ----------------------------------------
def disconnect():
    client.disconnect()


# ----------------------------------------
# Converts raw bits from a message --> str
# ----------------------------------------
def decode(message):
    #return bytes.decode(message)
    return message


# ----------------------------------------
# Converts message --> data for transmission
# ----------------------------------------
def encode(message):
    return message


# Client Setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
