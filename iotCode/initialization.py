import paho.mqtt.client as mqtt
import sys
sys.path.append("/home/pi/Desktop/IOT_Capstone/Code/iot_capstone22/")
import iotComm as comm
import time
import json
import subprocess
import os

CHANNELS = [ ("setup", 0), ]
ID_FILE = "/home/pi/Desktop/IOT_Capstone/Data/Pi_Data.txt" #Pi data
CRONTAB = "/home/pi/Desktop/IOT_Capstone/Data/crontab_TEMP.txt" #temp file for cronjobs
WATCHDOG = "/home/pi/Desktop/IOT_Capstone/Data/Watchdog/Watchdog_Scripts.txt" #watchdog scripts

# Generate message ID
def gen_message_id():
    message_time = time.time()
    hostname = comm.getHostname()
    message_id = hostname + str(message_time)
    return str(hash(message_id))

#save dictionary to file
def saveDictionary(dictionary, filename):
    out_file = open(filename, "w")
    json.dump(dictionary, out_file, sort_keys=True, indent=4)
    out_file.close()
    
message_id = gen_message_id()
id_set = False
crontab_set = False
watchdog_set = False


def on_message(client, someData, message):
    global id_set
    global crontab_set
    global watchdog_set
    if message.topic == CHANNELS[0][0]:
        data = str(message.payload.decode("utf-8"))
        #print(data)
        jsonObject= json.loads(data)
        if jsonObject["receiver_id"] == message_id:
            if not id_set:
                saveDictionary(json.loads(jsonObject["data"]), ID_FILE)
                print("Writing: " + jsonObject["data"] + " to " + ID_FILE)
                id_set = True
            elif not crontab_set:
                #get user and root cronjobs
                sudoBuffer = ""
                userBuffer = ""
                crons = json.loads(jsonObject["data"])
                for job in crons["sudo"].split("\n"):
                    sudoBuffer = sudoBuffer + job + "\n"
                for job in crons["user"].split("\n"):
                    userBuffer = userBuffer + job + "\n"
                    
                #Root crontab
                with open(CRONTAB, "wt") as fptr:
                    fptr.write(sudoBuffer)
                subprocess.call(['/usr/bin/crontab', '-u', 'root', CRONTAB])
                print("Root Crontab:")
                print(subprocess.check_output(['/usr/bin/crontab', '-u', 'root', '-l']).decode("utf-8"))
                
                #User crontab
                with open(CRONTAB, "wt") as fptr:
                    fptr.write(userBuffer)
                current_user = subprocess.check_output(['/usr/bin/who', '-u']).decode("utf-8").split(" ")[0].strip()
                subprocess.call(['/usr/bin/crontab', '-u', current_user, CRONTAB])
                print("User Crontab:")
                print(subprocess.check_output(['/usr/bin/crontab', '-u', current_user, '-l']).decode("utf-8"))
                
                #delete temp file
                os.remove(CRONTAB)
                
                #Done
                crontab_set = True
            elif not watchdog_set:
                #write to watchdog scripts file
                if jsonObject["data"] == "None":
                    watchdog_set = True
                else:
                    with open(WATCHDOG, "wt") as fptr:
                        fptr.write(jsonObject["data"])
                    print("Watchdog Scripts:")
                    print(jsonObject["data"])
                    print("Writing to " + WATCHDOG)
                    watchdog_set = True
                
    
def on_connect(client, userdata, flags, rc):
    print("Connected. Subscribing to:", CHANNELS)
    client.subscribe(CHANNELS)
    
    

print("Connecting to MQTT Server...")
comm.client.on_connect = on_connect
comm.client.on_message = on_message

while (True):
    try:
        start_time = time.time()
        comm.client.connect(comm.MQTT_SERVER_IP)
        comm.send(CHANNELS[0][0], "UNDEFINED", "UNDEFINED", comm.C2_ID, message_id)
        print("Listening for messages on:", CHANNELS)
        comm.client.loop_forever()
    except Exception as e:
        print("Connection failed after " + str(time.time()-start_time) + " seconds.")
        print(e)
        time.sleep(10)
    comm.client.disconnect()
    comm.client.loop_stop()