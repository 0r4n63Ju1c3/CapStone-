# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 11:00:50 2021

@author: C22Turner.Nims
"""

#monitor mqtt, check data against beacons saved in file

import paho.mqtt.client as mqtt
import datetime, time, random
import math
import json
from datetime import datetime
import sys
sys.path.append("/home/pi/Desktop/IOT_Capstone/Code/iot_capstone22/")
import iot_lib
import iotComm as comm

CONST_FILE = "/home/pi/Desktop/IOT_Capstone/Data/Pi_Data.txt" #pi data

#import dictionary from file
def readData(filename):
    data = {}
    try:
        f = open(filename, 'r')
        data = json.load(f) 
    except Exception as e:
        print(e)
        print("Error opening file: ", filename)  
    return data

PI_DATA = readData(CONST_FILE)
my_id = PI_DATA["ID"]
my_location = PI_DATA["LOCATION"]

#this is called when a message is received
def on_message(client, userdata, message):
    if message.topic == CHANNELS[0][0]:
        try:
            data = json.loads(str(message.payload.decode("utf-8")))
            #print(data)
            
            beacons = data["data"]
            for beacon_id in beacons.split(","):
                current_id = beacon_id.replace("'","").replace("[","").replace("]","")
                
                if current_id in beacon_ids:
                    #print("Found: " + current_id)
                    #one of the beacons reported by mqtt matches our database
                    index = beacon_ids.index(current_id)
                    user_id = pi_ids[index]
                    user_loc = data["location"]
                    pi_message = {"LOCATION": user_loc}
                    #print("Sending: " + str(pi_message))
                    comm.send("eInk_all", my_id, my_location, user_id, json.dumps(pi_message))
                    
                
        except Exception as e:
            print(e)

def on_connect(client, userdata, flags, rc):
    print("Connected. Subscribing to:", CHANNELS)
    client.subscribe(CHANNELS)

DATA_FILE = "/home/pi/Desktop/IOT_Capstone/Data/BlueTooth/Beacon_Data.json"

try:
    f = open(DATA_FILE, 'r')   
except Exception as e:
    print(e)
    print("Error opening file: ", DATA_FILE)
    
beacons = json.load(f)    
print(beacons)

#data arrays
beacon_ids = []
owners = []
pi_ids = []
locations = []

for data in beacons["BEACON"]:
    beacon_ids.append(data)
    
for data in beacons["OWNER"]:
    owners.append(data)
    
for data in beacons["PID"]:
    pi_ids.append(data)
    
for data in beacons["LOCATION"]:
    locations.append(data)
    


#listen on mqtt
CHANNELS = [ ("bluetooth_all", 0), ]
print("Connecting to MQTT Server...")
comm.client.on_connect = on_connect
comm.client.on_message = on_message

while (True):
    try:
        comm.client.connect(comm.MQTT_SERVER_IP)
        start_time = time.time()
        print("Listening for messages on:", CHANNELS)
        comm.client.loop_forever()
    except:
        print("Connection failed after " + str(time.time()-start_time) + " seconds.")
        time.sleep(10)
    comm.client.disconnect()
    comm.client.loop_stop()
    
# client_name = "bluetooth_listener"
# server_ip = "96.66.89.56" #public ip address of mqtt server
# channel_name = "eInk_all"
# #this is what to do when a message is sent on the mqtt channel
# def on_message(client, userdata, message):
#     
#     #get whole message from mqtt
#     data = str(message.payload.decode("utf-8")) #read data as string
#     json_dictionary = json.loads(data) #load string into dictionary
#     
#     #separates mqtt message into fields
#     device_id = json_dictionary["device_id"]
#     devices_found = json_dictionary["devicesFound"]
# 
#     #iterate through each device found by bluetooth tracker
#     for i in range(len(devices_found)):
#         
#         data_dictionary = {
#             "type": "bluetooth",
#             "found": devices_found[i]
#             }
#         
#         #publish that device into bluetooth column of database
#         response = iot_lib.upload_data(data_dictionary, device_id, api_key=12345)
#             
#         print(response)
#     
#     for device in devices_found:
#         try:
#             new_id = beaconsToTrack[device]
#             new_loc = json_dictionary["location"]
#             client.publish(channel_name, "ID:" + new_id + ",location:" + new_loc, qos=0)
#         except Exception as e:
#             print(e)
#         
#         
# 
# #MAIN
# #set up MQTT
# client = mqtt.Client(client_id = client_name)
# client.connect(server_ip)
# client.on_message = on_message #tells MQTT what to do when a message is received
# client.subscribe(channel_name, qos = 0) #subscribes to weatherPi channel
# print("started")
# #client.publish(channel_name, "hello world", qos=0)
# #(iot_lib.get_data("weather"))
# 
# #listen for message
# client.loop_start()
# 
# while True:
#     print("Heartbeat\t" + datetime.now().strftime("%B %d, %Y   %H:%M:%S"))
#     time.sleep(10)