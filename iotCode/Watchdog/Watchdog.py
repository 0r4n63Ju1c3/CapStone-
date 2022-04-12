from datetime import datetime
import requests
import subprocess
import paho.mqtt.client as mqtt
import psutil
import socket
import json
import fcntl
import struct

LOG_FILE = "/home/pi/Desktop/IOT_Capstone/Data/Watchdog/Watchdog_Data.txt"
SCRIPT_FILE = "/home/pi/Desktop/IOT_Capstone/Data/Watchdog/Watchdog_Scripts.txt"
CHANNEL = "status"
IP = "96.66.89.56"
MY_ID = socket.gethostname() #This ID may need to be retrieved from the ID file, same as e-ink_display.py.

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def startScript(script):
    result = "Done."
    try:
        subprocess.Popen("python3 " + script, shell = True)
    except Exception as e:
        result = "Error: " + str(e)
    return result

def checkScripts(filename):
    scripts = []
    alive = []
    report = ""
    f = open(filename, "rt")
    for line in f.readlines():
        scripts.append(line.strip())
    f.close()
    
    for p in psutil.process_iter():
        if "python" in p.name():
            for s in scripts:
                if len(p.cmdline())>1 and s in p.cmdline():
                    alive.append(s)
    
    for s in alive:
        print("ALIVE: " + s)
        report = report + "ALIVE: " + s + "\n"
        scripts.remove(s)
    
    for s in scripts:
        print("DEAD:  " + s)
        report = report + "DEAD:  " + s + "\n"
        
        #restart dead script
        text = "\tStarting script...\n"
        print(text)
        report = report + text
        
        text = "\t" + startScript(s) + "\n"
        print(text)
        report = report + text
                    
    return(report)

try:
    client = mqtt.Client(client_id=MY_ID)
    url = IP
    channel = CHANNEL
    client.connect(url)

    text = "====Watchdog Executing====\n" + datetime.now().strftime("%B %d, %Y   %H:%M:%S") + "\n\nChecking wifi connection...\n`"
    print(text)
    output = text

#     try:
#         #check wifi connectivity
    wifi = subprocess.check_output(['/usr/sbin/iwgetid']).decode("utf-8")
    essid = wifi.split('"')[1]
    
#         text = "Connected to " + essid + "\n\nChecking connection to " + url + "..."
#         print(text)
#         output = output + text
#         
#         #check server connection
#         check = subprocess.call(['/usr/bin/ping', '-w', '1', url])
#         if check == 0:
#             print("\nSuccessfully pinged " + url + ".\n")
#             output = output + "\nSuccessfully pinged " + url + ".\n\n"
#         else:
#             print("\nNo response from " + url + ", checking internet connection...")
#             output = output + "\nNo response from " + url + ", checking internet connection...\n"
#             try:
#                 #check internet connection
#                 request = requests.get("http://www.google.com", timeout=5)
#                 print("Connected to the internet.")
#                 output = output + "Connected to the internet.\n"
#             except (requests.ConnectionError, requests.Timeout) as exception:
#                 print("No internet connection.")
#                 output = output + "No internet connection.\n"
#     except Exception as e:
#         print("No wifi connection.")
#         output = output + "No wifi connection.\n"
#        print(e)

    #check scripts
    print("Checking scripts...\n")
    output = output + "Checking scripts...\n"
    output = output + checkScripts(SCRIPT_FILE)
    
    f = open(LOG_FILE, "a")
    f.write(output + "\n\n")
    f.close()
    
    #TODO generate some kind of output for the mqtt server
    ping_message = {}
    ping_message['deviceID'] = MY_ID
    ping_message['timestamp'] = str(datetime.today())
    ping_message['ssid'] = essid
    ping_message['ipaddress'] = get_ip_address()

    client.publish(CHANNEL, str(json.dumps(ping_message)), qos=0)
    print("MQTT Telemetry: ", ping_message)
    
except Exception as e:
    print(e)
    f = open(LOG_FILE, "a")
    f.write(datetime.now().strftime("%B %d, %Y   %H:%M:%S") + "\nError in Watchdog:\n" + str(e))
    f.close()
    

