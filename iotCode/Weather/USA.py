"""
MQTT Light Demo
Author:  Lt Col Adrian A. de Freitas
Description:  Shows an example of how to control nanoleaf
              lights using MQTT messages
              
              Nanoleaf API is available at:
              https://nanoleafapi.readthedocs.io/en/latest/
"""
from nanoleafapi import Nanoleaf, NanoleafDigitalTwin
import paho.mqtt.client as mqtt
import datetime, time, random
import math

# This object controls the entire nanoleaf array
# DFCS Entryway Lights:  "192.168.1.83" on Skynet-6
# DFCS Breakroom Lights:  "192.168.1.84" on Skynet-6
# Hexagons on 2nd Floor ACCR = "10.1.100.227")
# Triangles on 2nd Floor ACCR = "10.1.100.93")
# Squares on 2nd Floor ACCR = "10.1.100.63")
# Cyber city = "10.1.100.12" 

nanoleaf_all = Nanoleaf("192.168.1.182") 

# This object controls individual lights in a nanoleaf array
try:
    nanoleaf_single = NanoleafDigitalTwin(nanoleaf_all)
    #print(nanoleaf_single)
    #print(nanoleaf_single.get_ids())
    #light array left to right
    lights = nanoleaf_single.get_ids()
    print(lights)
except Exception as e:
    print(e)

#51239, 51544, 38038, 996, 23186, 48848, 2877, 6038, 64470, 30088, 39253, 43520, 23197, 9483, 64089, 0
 # This sets an individual light
client = mqtt.Client(client_id="nano_demo_app")


# Connects to the MQTT Broker


# Tells the client what function to call when a message
# is received
#client.on_message = on_message

# Publishes (i.e., sends) a message on a channel
# See MQTT documentation for Quality of Service (qos)
#client.publish("s_test2", "goodbye USAFA", qos=0)

# Subscribes to a Topic to Receive Messages
#client.subscribe("weather_temp", qos=0)
cycle = 0
n = 254
direction = 0
zero = (random.randint(0,2))
one = (random.randint(0,2))
two = (random.randint(0,2))
three = (random.randint(0,2))
four = (random.randint(0,2))
five = (random.randint(0,2))
six = (random.randint(0,2))

red = (n,0,0)
white = (n,n,n)
blue = (0,0,n)
clear = (0,0,0)
color = [red,white,blue,clear]




while (1):
    if n > 248:
        direction = 1
    if n < 6:
        nanoleaf_single.set_color(lights[0], color[3])
        nanoleaf_single.set_color(lights[1], color[3])
        nanoleaf_single.set_color(lights[2], color[3])
        nanoleaf_single.set_color(lights[3], color[3])
        nanoleaf_single.set_color(lights[4], color[3])
        nanoleaf_single.set_color(lights[5], color[3])
        nanoleaf_single.set_color(lights[6], color[3])
        nanoleaf_single.sync()
        time.sleep(1)
        direction = 0
        zero = (random.randint(0,2))
        one = (random.randint(0,2))
        two = (random.randint(0,2))
        three = (random.randint(0,2))
        four = (random.randint(0,2))
        five = (random.randint(0,2))
        six = (random.randint(0,2))
        cycle = cycle + 1
        if cycle > 6:
            cycle = 0
 
    if direction == 0:
        n = n+5
        red = (n,0,0)
        white = (n,n,n)
        blue = (0,0,n)
        color = [red,white,blue,clear]
    else:
        n = n-5
        red = (n,0,0)
        white = (n,n,n)
        blue = (0,0,n)
        color = [red,white,blue,clear]
     

    nanoleaf_single.set_color(lights[0], color[zero])
    nanoleaf_single.set_color(lights[1], color[one])
    nanoleaf_single.set_color(lights[2], color[two])
    nanoleaf_single.set_color(lights[3], color[three])
#     nanoleaf_single.set_color(lights[4], color[four])
#     nanoleaf_single.set_color(lights[5], color[five])
#     nanoleaf_single.set_color(lights[6], color[six])
        
    time.sleep(.05)
    nanoleaf_single.sync()
   





