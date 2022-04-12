#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import paho.mqtt.client as mqtt
import requests
from datetime import datetime
import time
sys.path.append("/home/pi/Desktop/IOT_Capstone/Code/iot_capstone22/")
import iotComm as comm
import json
from PIL import Image,ImageDraw,ImageFont

#eink library and font
fontdir = "/home/pi/Desktop/IOT_Capstone/Data/eInk/font"
libdir = "/home/pi/Desktop/IOT_Capstone/Data/eInk/lib"
if os.path.exists(libdir):
    sys.path.append(libdir)
    
from waveshare_epd import epd7in5_V2

#data files
DATA_FILE = "/home/pi/Desktop/IOT_Capstone/Data/eInk/eInk_Data.txt" #eInk display data
ID_FILE = "/home/pi/Desktop/IOT_Capstone/Data/Pi_Data.txt" #Pi data

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
        

#load data from files
PI_DATA = readData(ID_FILE)
EINK_DATA = readData(DATA_FILE)

#set constants
PI_ID = PI_DATA["ID"]
PI_LOCATION = PI_DATA["LOCATION"] 
BG_FILE = EINK_DATA["BG_FILE"]
IMAGE_FILE = EINK_DATA["IMAGE_FILE"]
PRIVACY = EINK_DATA["PRIVACY"]

CHANNELS = [ ("eInk_all", 0), ]
USERNAME = "2021Cap"
PASSWORD = "grindn3v3rstops"

LOGIN_URL = "https://iot.dfcs-cloud.net/login.php"
URL = "https://iot.dfcs-cloud.net/"

LOCAL = "LOCAL" #where is the image stored?

#privacy
NONE = "NONE" #don't show any location info
BASIC = "BASIC" #show only here or away based on BT data
FULL = "FULL" #show exact location based on BT data

#default display
DISPLAY_WIDTH = 0 #set later
DISPLAY_HEIGHT = 0 #set later
EINK_DISPLAY = {
        "FACULTY NAME" : "Name",
        "TITLE" : "Job",
        "LOCATION" : "???",
        "MESSAGE" : "Message",
        "PICTURE" : LOCAL
        }
    
#fonts
font24 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 24)
font18 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 18)
font48 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 48)

#update dictionary with data from another dictionary
def updateDictionary(working_dict, new_dict):
    final_dict = {}
    for k in working_dict.keys():
        if k in new_dict.keys():
            final_dict[k] = new_dict[k]
        else:
            final_dict[k] = working_dict[k]
    return final_dict

#save dictionary to file
def saveDictionary(dictionary, filename):
    out_file = open(filename, "w")
    json.dump(dictionary, out_file, sort_keys=True, indent=4)
    out_file.close()

#Update display from file
EINK_DISPLAY = updateDictionary(EINK_DISPLAY, EINK_DATA)
#print(EINK_DISPLAY)

#downloads picture from the web
def getPicture(path):
    global IMAGE_FILE
    session_requests = requests.session()
    # Get login csrf token
    result = session_requests.get(LOGIN_URL)

    # Create payload
    payload = {
        "username":USERNAME, 
        "password":PASSWORD, 
    }

    # Perform login
    result = session_requests.post(LOGIN_URL, payload)

    # Scrape url
    result = session_requests.get(URL+path)
    f_ext = os.path.splitext(URL+path)[-1].lower()
    
    if f_ext in {".jpg", ".jpeg", ".png", ".bmp"}:
        IMAGE_FILE = IMAGE_FILE.split(".")[0] + f_ext
        with open(IMAGE_FILE, 'wb') as f:
            f.write(result.content)
    else:
        raise Exception("Could not resolve file type.")


#returns an image created from inputs
def createImage(name, title, message, location, picture, size):
    global EINK_DISPLAY
    im = Image.new('1', (size[0], size[1]), 255)  # 255: clear the frame
    #background
    bg = Image.open(BG_FILE)
    bg_width, bg_height = bg.size
    w_scale = size[0]/bg_width
    h_scale = size[1]/bg_height
    
    #profile pic
    if not picture == LOCAL:
        try:
            getPicture(picture) #download picture from web
            EINK_DISPLAY["PICTURE"] = LOCAL
            
            EINK_DATA["IMAGE_FILE"] = IMAGE_FILE
            EINK_DATA["PICTURE"] = LOCAL
            saveDictionary(EINK_DATA, DATA_FILE)
        except Exception as e:
            print(e)
            print("Failed to update picture.")
    
    
    pic_x = 25 #picture x location
    pic_y = 104 #picture y location
    pb_width = 280 #
    pb_height = 346
    im.paste(bg.resize((size[0], size[1])), (0,0))
    pic = Image.open(IMAGE_FILE)
    im.paste(pic.resize((int(pb_width*w_scale),int(pb_height*h_scale))), (int((pic_x+1)*w_scale),int((pic_y+1)*h_scale)))
    draw = ImageDraw.Draw(im)
    
    #Name and title
    draw.text((32, 0), name, font = font48, fill = 0)
    draw.text((36, 50), title, font = font24, fill = 0)
    
    #Message
    num_lines = 17 #the textbox can fit 17 lines 
    line_size = 20 #lines are 20 pixels
    tb_x = 330 #textbox x location
    tb_y = 108 #textbox y location
    tb_width = 440 #textbox width
    line_number = 0
    message_array = message.split("\n")
    for text in message_array:
        text = text + " "
        chars_remaining = len(text)
        line_start = 0
        line_end = chars_remaining
        #print(font18.getsize(message[line_start:line_end])[0])
        while chars_remaining > 0:
            while font18.getsize(text[line_start:line_end])[0] > tb_width:
                line_end = line_end-1
            #line is correct length
            #backtrack lo last space
            #print(message[line_end-1])
            temp = line_end
            while text[line_end-1] != " ":
                line_end = line_end-1
                if line_end == -1:
                    line_end = temp
                    break
            line = text[line_start:line_end] + " "
            draw.text((tb_x, tb_y+line_number*line_size), line, font = font18, fill = 0)
            line_start = line_end
            chars_remaining = chars_remaining - len(line)
            line_end = line_end + chars_remaining + 1
            line_number = line_number+1
            if line_number == num_lines:
                chars_remaining = 0
        
        if line_number == num_lines:
            break
    
    #location
    if PRIVACY==FULL:
        #show full location data
        loc = location
    elif PRIVACY==BASIC:
        #show basic location data (here or away)
        if location==PI_LOCATION:
            loc = "Here"
        else:
            loc = "Away"
    else:
        #do not show location
        loc = ""
    
    #draw text
    draw.text((600, 10), loc, font = font24, fill = 0)
        
    return im

#displays an image using dictionary
def displayImage(dictionary):
    try:
        EINK = epd7in5_V2.EPD()
        EINK.init()
        EINK.Clear()
        displaySize = (EINK.width, EINK.height)
        einkImage = createImage(dictionary["FACULTY NAME"], dictionary["TITLE"], dictionary["MESSAGE"], dictionary["LOCATION"], dictionary["PICTURE"], displaySize)
        EINK.display(EINK.getbuffer(einkImage))
        time.sleep(2)
        EINK.sleep()

    except Exception as e:
        print("Error initializing eInk display.")
        print(e)
        epd7in5_V2.epdconfig.module_exit()
        return

    

#this is called when a message is received
def on_message(client, userdata, message):
    global EINK_DISPLAY
    #print(message.topic)
    if message.topic == CHANNELS[0][0]:
        data = str(message.payload.decode("utf-8"))
        #check for pi id
        if PI_ID in data:
            data_obj = json.loads(data)
            if data_obj["receiver_id"] == PI_ID:
                print("Message: " + data)
                parsed_data = json.loads(data_obj["data"])
                print(parsed_data)
                
                #update EINK_DISPLAY
                for key in parsed_data.keys():
                    if not key=="ID":
                        EINK_DISPLAY[key] = parsed_data[key]
                
                #update display
                if "FILE PATH" in parsed_data.keys():
                    EINK_DISPLAY["PICTURE"] = parsed_data["FILE PATH"]
                displayImage(EINK_DISPLAY)
                
                #update data file
                updateDictionary(EINK_DATA, EINK_DISPLAY)
                saveDictionary(EINK_DATA, DATA_FILE)

def on_connect(client, userdata, flags, rc):
    print("Connected. Subscribing to:", CHANNELS)
    client.subscribe(CHANNELS)
    
    
############
# MAIN
############
print("PI ID: " + PI_ID)
print("PI Location: " + PI_LOCATION)

try:
    try:
        getPicture(EINK_DATA["FILE PATH"])
    except:
        print("Could not download picture.")
        
    displayImage(EINK_DISPLAY)

except Exception as e:
    print(e)
    epd7in5_V2.epdconfig.module_exit()
    exit()

print("Connecting to MQTT Server...")
comm.client.on_connect = on_connect
comm.client.on_message = on_message

while (True):
    try:
        start_time = time.time()
        comm.client.connect(comm.MQTT_SERVER_IP)
        print("Listening for messages on:", CHANNELS)
        comm.client.loop_forever()
    except Exception as e:
        print("Connection failed after " + str(time.time()-start_time) + " seconds.")
        print(e)
        time.sleep(10)
    comm.client.disconnect()
    comm.client.loop_stop()