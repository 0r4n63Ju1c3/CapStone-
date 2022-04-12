import requests
import time

#pull beacon list from web and save to file

FILE_NAME = '/home/pi/Desktop/IOT_Capstone/Data/BlueTooth/Beacon_Data.json'

page = requests.get("https://iot.dfcs-cloud.net/bluetoothJSON.php?apiKey=12345")
#print(page.text)

try:
    f = open(FILE_NAME, 'w+')
    f.write(page.text)
    f.close()
    #print(page.text)
except Exception as e:
    print(e)
    print("Error opening file: ", DATA_FILE)


# --------------------------------------------------------------
# A simple dictionary to keep track of relevant BLE MACs
# Without this, you will get overwhelmed
# --------------------------------------------------------------
# import json
# beaconData = {}
# beaconData['Beacon Info'] = []
#Pull once per day from online/database
# beaconsToTrack = { }
# beaconsReported = set()

# x = requests.get("https://iot.dfcs-cloud.net/bluetoothJSON.php?apiKey=12345")
# print(x)
# webjson = x.json()
# 
# for entry in webjson["BEACON"]:
#     beaconsToTrack[webjson["BEACON"][entry]] = webjson["OWNER"][entry]
# with open ('/home/pi/Desktop/beaconsList.json', 'w') as outfile:
#     json.dump(beaconsToTrack, outfile)
