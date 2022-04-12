import paho.mqtt.client as mqtt
import sys
sys.path.append("/home/pi/Desktop/IOT_Capstone/Code/iot_capstone22/BlueTooth/")
sys.path.append("/home/pi/Desktop/IOT_Capstone/Code/iot_capstone22/")
import iotComm as comm
import iot_lib
import blescan
import datetime
import bluetooth._bluetooth as bluez
import time
import json
import requests
import bcrypt

CHANNELS = CHANNELS = [ ("setup", 0), ]
ID_FILE = "/home/pi/Desktop/IOT_Capstone/Data/Pi_Data.txt" #Pi data
CRON_FILE = "/home/pi/Desktop/IOT_Capstone/Data/Crontab_Data.txt" #crontab in json format
EINK_URL = "https://iot.dfcs-cloud.net/eInkJSON.php?apiKey=12345" #eink data url
USER_URL = "https://iot.dfcs-cloud.net/usersJSON.php?apiKey=12345" #user data url

#bluetooth scan
SCAN_TIME = 3 # Specifies how long the scan can run (in seconds)
sock = None # bluetooth socket


def readData(filename):
    data = {}
    try:
        f = open(filename, 'r')
        data = json.load(f) 
    except Exception as e:
        print(e)
        print("Error opening file: ", filename)  
    return data

#load data from files
PI_DATA = readData(ID_FILE)


#prepare bluetooth scanner
def start_scanner():
    global sock
    dev_id = 0
    try:
        sock = bluez.hci_open_dev(dev_id)
    except:
        print ("Error accessing bluetooth device...")
        sys.exit(1)
    blescan.hci_le_set_scan_parameters(sock)
    blescan.hci_enable_le_scan(sock)

#scan bluetooth for a time duration
def bluetoothScan(duration):
    currentDate = datetime.datetime.now()
    stopDate = datetime.datetime.now() + datetime.timedelta(seconds=duration)

    beaconsReported = []
    while currentDate < stopDate:
        beaconsFound = blescan.parse_events(sock, 10)
        
        for beacon in beaconsFound:
            beaconAttributes = beacon.split(",")
            if (beaconAttributes[1] not in beaconsReported):
                beaconsReported.append(beaconAttributes[1])
                #print(beaconAttributes[1])
            currentDate = datetime.datetime.now()
    return beaconsReported

#user picks bluetooth id from scan list
def findByScan():
    valid = False
    output = ""
    while not valid:
        beaconsFound = bluetoothScan(SCAN_TIME)
        print("\nScan Complete\n")
        for b in beaconsFound:
            print(b)
        print("\n")
        part = str(input("Enter partial beacon: "))
        index = 1
        matches = []
        for beacon in beaconsFound:
            if part in beacon:
                matches.append(beacon)
                print("(" + str(index) + ") " + beacon)
                index = index + 1
        if index == 1:
            #no matches
            print("No matches: " + part)
            choice = str(index)
        else:
            print("(" + str(index) + ") Not Listed")
            choice = input("Enter a number: ")
            
        if not (choice.isnumeric() and 0 < int(choice) <= index):
            print("Invalid input: " + choice)
        elif choice == str(index):
            #Not listed
            option_valid = False
            while not option_valid:
                print("\n")
                print("(1) Scan again\n(2) Manual entry")
                option = input("Enter a number: ")
                if not (option == "1" or option == "2"):
                    print("Invalid input: " + option)
                elif option == "1":
                    #do nothing
                    option_valid = True
                elif option == "2":
                    output = input("Enter bluetooth ID: ")
                    option_valid = True
                    valid = True
        else:
            #listed choice
            output = matches[int(choice)-1]
            valid = True
            
    return output    
    
#get bluetooth id from user    
def getBluetooth():
    valid = False
    output = ""
    while not valid:
        print("\n=Bluetooth Setup=")
        print("(1) Local Scan\n(2) Manual Entry")
        choice = input("Enter a number: ")
        if not (choice == "1" or choice == "2"):
            print("Invalid input: " + choice)
        elif choice == "1":
            #scan
            output = findByScan()
            valid = True
            
        elif choice == "2":
            #user input
            output = input("Enter bluetooth ID: ")
            valid = True
    return output


#update user table
def updateUsers(user_id, username, password, device_id):
    dictionary = {}
    dictionary["id"] = user_id
    dictionary["username"] = username
    dictionary["password"] = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode("utf-8")
    dictionary["device_id"] = device_id
    try:
        print("Updating Database.")
        print(iot_lib.update_data(dictionary, user_id, 12345, "users", user_id))
    except Exception as e:
        print("Error updating database.")
        print(e)

#update bluetooth in database
def updateBluetooth(beacon, pi_id, location):
    dictionary = {}
    dictionary["BLUETOOTH_ID"] = beacon
    dictionary["PI_ID"] = pi_id
    dictionary["PI_LOCATION"] = location
    print("\nBeacon Info:")
    for key in list(dictionary.keys()):
        string = key + ": "
        print(string.rjust(14) + dictionary[key])
    print(" ")
    name = input("Enter beacon owner: ")
    dictionary["BT_OWNER"] = name
    try:
        print("Updating Database.")
        print(iot_lib.update_data(dictionary, beacon, 12345, "known_bt", beacon))
    except Exception as e:
        print("Error updating database.")
        print(e)

#update database
def updateDatabase(new_data):
    print("Updating Database.")
    try:
        device_id = str(int(new_data["ID"].split("eInk_Pi")[1]))
        dictionary = {
            "LOCATION": new_data["LOCATION"],
            "ID": device_id,
            "FACULTY_NAME": "No Data",
            "TITLE": "No Data",
            "MESSAGE": "No Data",
            "FILE_PATH": "No Data"
            }
        
        #update_data(data_dictionary, device_id, api_key=12345, table_name, row_id):
        print(iot_lib.update_data(dictionary, device_id, 12345, "eink_messages", device_id))
    except Exception as e:
        print("Error updating database.")
        print(e)


#get id from user or database
def getID():
    output = "UNDEFINED"
    valid = False
    while not valid:
        print("\n=Pi ID Setup=")
        print("(1) eInk Display\n(2) Weather Station\n(3) Other")
        value = input("Enter a number: ")
        if value == "1":
            #get next available eink from database
            try:
                print("Contacting web server.")
                session_requests = requests.session()
                result = session_requests.get(EINK_URL)
                eink_ids = json.loads(result.text)["ID"]
                new_id = 1
                while str(new_id) in eink_ids:
                    new_id = new_id + 1
                #id found
                output = "eInk_Pi" + str(new_id).zfill(7) #IDs are saved in the database as numbers, so we need to add the eInkPi identifier
                print("ID available: " + output)
                
            except Exception as e:
                print("Failed to get ID.")
                print(e)
                
            valid = True
            
        elif value == "2":
            #get next available weather from database
            #TODO: wtf is going on with weather???
            valid = True
            
        elif value == "3":
            output = input("Custom ID: ")
            valid = True
            
        else:
            print("Invalid input: " + value)
    
    return output


def getUserInput():
    roomNum = input("Location: ")
    pi_ID = getID()
    userData = {"LOCATION" : roomNum, "ID" : pi_ID}
    updateDatabase(userData)
    return userData

#user select crontab from file 
def getCrontab(dictionary):
    valid = False
    while not valid:
        output = {}
        sudo_cron = ""
        user_cron = ""
        index = 1
        keys = list(dictionary.keys())
        print("\n=Crontab Setup=")
        for key in keys:
            print("(" + str(index) + ") " + key)
            index = index + 1
        choice = input("Enter number(s): ")
        for char in choice:
            if char.isnumeric() and 0 < int(char) <= len(keys):
                if not keys[int(char)-1] == "Github":
                    sudo_cron = sudo_cron + "\n#" + keys[int(char)-1] + "\n" + dictionary[keys[int(char)-1]] + "\n"
                    valid = True
                else:
                    user_cron = user_cron + "\n#" + keys[int(char)-1] + "\n" + dictionary[keys[int(char)-1]] + "\n"
                    valid = True
            else:
                print("Invalid input: " + char)
                valid = False
                break
    output = {"sudo": sudo_cron, "user": user_cron}
    return json.dumps(output)

#get watchdog scripts
def getWatchdog(initial):

    #initial is a string of the initial watchdog
    scripts = []
    for line in initial.split("\n"):
        if not line == "":
            scripts.append(line)
    
    #get user input
    valid = False
    while not valid:
        print("\nWatchdog scripts:")
        for s in scripts:
            print(s)
        print("\n=Watchdog Setup=\n(1) Accept and Send\n(2) Add\n(3) Remove")
        choice = input("Enter a number: ")
        if len(choice) == 1 and choice.isnumeric():
            if choice == "1":
                #done
                valid = True
            elif choice == "2":
                #add line
                new = input("Add: ")
                scripts.append(new)
            elif choice == "3":
                #remove line
                remove_valid = False
                while not remove_valid:
                    index = 1
                    print("\n=Delete Options=")
                    for s in scripts:
                        print("(" + str(index) + ") " + s)
                        index = index + 1
                    remove = input("Enter number(s): ")
                    for char in remove:
                        if char.isnumeric() and 0 < int(char) <= len(scripts):
                            scripts.pop(int(char)-1)
                            remove_valid = True
                        else:
                            print("Invalid input: " + char)
                            remove_valid = False
            else:
                print("Invalid input: " + choice)
        else:
            print("Invalid input: " + choice)
    
    output = ""
    for s in scripts:
        output = output + s + "\n"
    return output

#gets username for website and checks that it isnt already in use
def getUsername():
    output = ""
    try:
        session_requests = requests.session()
        result = session_requests.get(USER_URL)
        users = str(json.loads(result.text)["username"])
    except Exception as e:
        print("Error accessing website.")
        print(e)
    
    valid = False
    while not valid:
        user = str(input("Username: "))
        if len(users) > 0 and user in users:
            print("Username " + user + " already exists.\n")
        else:
            output = user
            valid = True
    
    return output
            

#this is called when a message is received
def on_message(client, someData, message):
    if message.topic == CHANNELS[0][0]:
        data = str(message.payload.decode("utf-8"))
        #print(data)
        jsonObject= json.loads(data)
        if jsonObject["receiver_id"] == PI_DATA["ID"]:
            
            #set up Pi_Data.txt
            session_id = jsonObject["data"]
            userData = getUserInput()
            comm.send(CHANNELS[0][0], PI_DATA["ID"], PI_DATA["LOCATION"], session_id, json.dumps(userData))
            print("Sending: " + json.dumps(userData))
            
            #set up Crontabs
            cron_json = json.load(open(CRON_FILE, "rt"))
            crons = getCrontab(cron_json)
            comm.send(CHANNELS[0][0], PI_DATA["ID"], PI_DATA["LOCATION"], session_id, crons)
            print("Sending: " + crons)
            
            #set up watchdog script
            if not "#Standard" in crons:
                print("No watchdog scripts.")
                comm.send(CHANNELS[0][0], PI_DATA["ID"], PI_DATA["LOCATION"], session_id, "None")
            else:
                watchdog_scripts = ""
                raw_scripts = json.loads(crons)["user"] + "\n" + json.loads(crons)["sudo"]
                for line in raw_scripts.split("\n"):
                    if "@reboot" in line and "python3" in line:
                        watchdog_scripts = watchdog_scripts + line.split("python3 ")[-1] + "\n"
                watchdog_scripts = getWatchdog(watchdog_scripts)
                comm.send(CHANNELS[0][0], PI_DATA["ID"], PI_DATA["LOCATION"], session_id, watchdog_scripts)
                print("Sending: " + watchdog_scripts)
            
            #set up bluetooth beacon
            bt_beacon = getBluetooth()
            updateBluetooth(bt_beacon, userData["ID"], userData["LOCATION"])
            
            #set up website login
            print("\n=Website Setup=")
            username = getUsername()
            password = input("Password: ")
            updateUsers(str(int(userData["ID"].split("eInk_Pi")[1])), username, password, userData["ID"])           

        
def on_connect(client, userdata, flags, rc):
    print("Connected. Subscribing to:", CHANNELS)
    client.subscribe(CHANNELS)
    
print("Connecting to MQTT Server...")
comm.client.on_connect = on_connect
comm.client.on_message = on_message

while (True):
    try:
        start_time = time.time()
        start_scanner() #prepare bluetooth scanner
        comm.client.connect(comm.MQTT_SERVER_IP)
        print("Listening for messages on:", CHANNELS)
        comm.client.loop_forever()
    except Exception as e:
        print("Connection failed after " + str(time.time()-start_time) + " seconds.")
        print(e)
        time.sleep(10)
    comm.client.disconnect()
    comm.client.loop_stop()