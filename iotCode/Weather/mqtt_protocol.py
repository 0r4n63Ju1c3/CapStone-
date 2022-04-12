import json
import subprocess
from datetime import datetime


def wrapMessage(pi_id, pi_location, data):

    try:
        #get wifi network
        ssid = subprocess.check_output(['/usr/sbin/iwgetid']).decode("utf-8").split(":")[-1].replace("\"", "").strip()
        #print(ssid)
        
        #get ip
        ip = subprocess.check_output(['/usr/sbin/ip', 'address']).decode("utf-8").split("wlan0:")[-1].split("inet ")[-1].split("/")[0]
        #print(ip)
    except Exception as e:
        #print(e)
        ssid = "Undefined"
        ip = "Undefined"
        
    #get time
    time = datetime.now().strftime("%B %d, %Y   %H:%M:%S")
    #print(time)
    
    dictionary = {
        "id": pi_id,
        "location": pi_location,
        "ssid": ssid,
        "ip": ip,
        "time": time,
        "data": data
        }
    #print(dictionary)
    return json.dumps(dictionary)
