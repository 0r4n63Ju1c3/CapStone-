from __future__ import print_function
# test BLE Scanning software
# SwitchDoc Labs December 2020 
# https://github.com/switchdoclabs/SDL_Pi_iBeaconScanner

import blescan
import sys
import time
import datetime
import bluetooth._bluetooth as bluez
import paho.mqtt.client as mqtt
import requests
sys.path.append("/home/pi/Desktop/IOT_Capstone/Code/iot_capstone22/")
import iot_lib
import iotComm as comm
import json

# Specifies how long the scan can run (in seconds)
SCAN_TIME = 3

# Socket
sock = None

# ----------------------------------------------------------
# Starts the BLE Scanner
# ----------------------------------------------------------
def start_scanner():
    global sock
    dev_id = 0
    try:
        sock = bluez.hci_open_dev(dev_id)
        print("----------------------------------")
        print("Bluetooth LE Thread Started")
        print("----------------------------------")
    except:
        print ("error accessing bluetooth device...")
        sys.exit(1)
    
    blescan.hci_le_set_scan_parameters(sock)
    blescan.hci_enable_le_scan(sock)

# -----------------------------------------------------------
# Main Program
# -----------------------------------------------------------

# Starts the scanner
start_scanner()
# Computes the Start and End Times
currentDate = datetime.datetime.now()
stopDate = datetime.datetime.now() + datetime.timedelta(seconds=SCAN_TIME)

beaconsReported = []
while currentDate < stopDate:
    # Retrieves the Beacons Found
#    print("Step 1")
    beaconsFound = blescan.parse_events(sock, 10)
#    print("Step 2")
    
    for beacon in beaconsFound:
        beaconAttributes = beacon.split(",")
        if (beaconAttributes[1] not in beaconsReported):
            beaconsReported.append(beaconAttributes[1])
            #print(beaconAttributes[1])
        currentDate = datetime.datetime.now()
        
    
# Prints a Message to Let Me Know the Nightmare Has Ended
print("\n\n-------------------------------------------------")
print("Scan Completed at ", currentDate)
print("-------------------------------------------------")
print("Found " + str(len(beaconsReported)) + " unique devices")


def on_connect(client, userdata, flags, rc):
    print("Connected. Subscribing to:", CHANNELS)
    client.subscribe(CHANNELS)

#connect to mqtt
CHANNELS = [ ("bluetooth_all", 0), ]
print("Connecting to MQTT Server...")
comm.client.on_connect = on_connect

comm.client.connect(comm.MQTT_SERVER_IP)


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




package = str(beaconsReported)
#package = str(["426c7565436861726d426561636f6e73"])
#print(package)

receiver = comm.C2_ID
comm.send(CHANNELS[0][0], my_id, my_location, receiver, package)
comm.disconnect()
#might be done


# # Initialize JSON file info so database knows what to do with beacon info
# beaconData = {}
# beaconData['Beacon Info'] = []
# 
# f = open('/home/pi/Desktop/rPiInfo4Scanner.json')
# piData = json.load(f)
# 
# client_name = piData['client_name']
# channel_name = piData['channel_name']
# server_ip = piData['server_ip'] #public ip address of mqtt server
# 

# 
# # --------------------------------------------------------------
# # A simple dictionary to keep track of relevant BLE MACs
# # Without this, you will get overwhelmed
# # --------------------------------------------------------------
# #Pull once per day from online/database
# beaconsToTrack = { }
# beaconsReported = set()
# 
# x = requests.get("https://iot.dfcs-cloud.net/bluetoothJSON.php?apiKey=12345")
# webjson = x.json()
# 
# for entry in webjson["BEACON"]:
#     beaconsToTrack[webjson["BEACON"][entry]] = webjson["OWNER"][entry]
#


# #print(beaconsToTrack)
# 
# 

# 
# def sendText(raw_data, sensor_id, quality):
#     client.publish(sensor_id, raw_data, qos=0)
#     
#     
# def on_message(client, userdata, message):
# 
#     data = str(message.payload.decode("utf-8")) #read data as string
# 
#     #parse data
#     deviceMAC, beaconID, location = parseData(data)
# 
#     #create dictionary of data
#     data_dictionary = {
#       "type": "known_bt",
#       "Device MAC": deviceMAC,
#       "BeaconID": beaconID,
#       "Location": location
#     }
# 
#     device_MAC = deviceMAC #assuming we want to clientname to be the deviceid in the database
# 
#     #upload to database
#     response = iot_lib.upload_data(data_dictionary, device_MAC, api_key=12345)
# 
#     print(response)
    
# #MAIN
# #set up MQTT
# client = mqtt.Client(client_id = client_name)
# client.connect(server_ip)
# client.on_message = on_message #tells MQTT what to do when a message is received
# client.subscribe(channel_name, qos = 0) #subscribes to eInk_all channel
# print("started")
# client.publish(channel_name, jsonString, qos=0)
# 
# # Send to MQTT
# # sendText(str(beaconsReported), "eInk_Bluetooth", 0)
# print("Successfully sent to MQTT!")