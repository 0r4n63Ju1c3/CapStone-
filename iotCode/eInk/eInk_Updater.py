import paho.mqtt.client as mqtt
import requests
import re
import os.path
import time
from datetime import datetime
import sys
sys.path.append("/home/pi/Desktop/IOT_Capstone/Code/iot_capstone22/")
import iotComm as comm
import json

LOG_FILE = "/home/pi/Desktop/IOT_Capstone/Data/eInk/eInk_Log.txt"

USERNAME = "2021Cap"
PASSWORD = "grindn3v3rstops"

LOGIN_URL = "https://iot.dfcs-cloud.net/login.php"
URL = "https://iot.dfcs-cloud.net/eInkJSON.php?apiKey=12345"


#MQTT stuff
CHANNELS = [ ("eInk_all", 0), ]
PI_ID = "IOT_C2"
LOCATION = "Capstone Room"

# ---------------------------------------------
# Runs on Connect
# ---------------------------------------------
def on_connect(client, userdata, flags, rc):
    print("Connected. Subscribing to channels:", CHANNELS)
    print()
        
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(CHANNELS)

#takes raw data and returns array of json strings
def parseData(raw):
    data = json.loads(raw)
    array = []
    for index in range(0, len(data[list(data.keys())[0]])):
        dictionary = {}
        for key in data.keys():
            if key=="ID":
                dictionary[key] = "eInk_Pi" + str(data[key][index]).zfill(7) #IDs are saved in the database as numbers, so we need to add the eInkPi identifier
            else:
                dictionary[key] = data[key][index]
        array.append(json.dumps(dictionary))
    #print(array)
    return array

#loads file, returns items in array that do not match file
def checkLog(filename, array):
    changes = []
    with open(filename, "r") as fptr:
        file_data = fptr.read().split("\n")
    
    if len(file_data[0]) == 0:
        return array #the log file is empty
    else:
        #check web data against file
        for line in array:
            if not line in file_data:
                changes.append(line)
        return changes 

#saves array text to file separated by newlines
def saveData(filename, array):
    output = ""
    with open(filename, "w") as fptr:
        for line in array:
            output = output + line + "\n"
        fptr.write(output.strip())
    
################
##MAIN
################
if not os.path.exists(LOG_FILE):
    print(LOG_FILE + " not found. Creating " + LOG_FILE)
    fptr = open(LOG_FILE, "a")
    fptr.write("")
    fptr.close()

while True:
    try:
        start_time = time.time()
        # MQTT Initialization
        comm.client.on_connect = on_connect
        print("Connecting to MQTT Server...")
        comm.client.connect(comm.MQTT_SERVER_IP)

        while True:       
            # Scrape url
            try:
                print("Contacting web server.")
                session_requests = requests.session()
                result = session_requests.get(URL)
                
                #parse data
                new_data = [] #list of json strings
                new_data = parseData(result.text)
                
                #check for changes
                changes = [] #list of changes to send out
                changes = checkLog(LOG_FILE, new_data)
                
                #send changes to mqtt
                if len(changes) > 0:
                    print("\nChanges found:")
                    print(changes)
                    for line in changes:
                        receiver = line.split("ID\": \"")[1].split("\",")[0]
                        comm.send(CHANNELS[0][0], PI_ID, LOCATION, receiver, line)
                else:
                    print("Up to date.")
                
                #save new data to file
                saveData(LOG_FILE, new_data)
                
            except Exception as e:
                print("Failed.")
                print(e)
                       
            wait = 10
            print("Sleep for {:d} seconds.\n".format(wait))
            time.sleep(wait)
            
    except Exception as e:
        print("Connection failed after " + str(time.time()-start_time) + " seconds.")
        print(e)
        time.sleep(10)
        comm.client.disconnect()
