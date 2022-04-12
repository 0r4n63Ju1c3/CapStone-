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
import encryption
import sys

# This object controls the entire nanoleaf array
# DFCS Entryway Lights:  "192.168.1.83" on Skynet-6
# DFCS Breakroom Lights:  "192.168.1.84" on Skynet-6
# 192.168.1.116
# total arguments
n = len(sys.argv)
print("Total arguments passed:", n)
 
# Arguments passed
print("\nName of Python script:", sys.argv[0])
 
print("\nArguments passed:", end = " ")
for i in range(1, n):
    print(sys.argv[i], end = " ")

#argv[1]
nanoleaf_all = Nanoleaf("192.168.1.124")

# This object controls individual lights in a nanoleaf array
nanoleaf_single = NanoleafDigitalTwin(nanoleaf_all)
print("Listening to MQTT server...")
print(nanoleaf_single.get_ids())
#light array left to right
lights = nanoleaf_single.get_ids()
print(lights)


#51239, 51544, 38038, 996, 23186, 48848, 2877, 6038, 64470, 30088, 39253, 43520, 23197, 9483, 64089, 0
#62926, 18230, 6487, 36139, 59658, 42639, 50977, 51324, 60486, 5499, 0
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



def on_message(client, userdata, message):
    """ Event Handler for when this program gets an MQTT Message.
        NOTE:  All subscribed topics are processed here

    Parameters
        ----------
        client
            The MQTT Client object
        userdata
            Information about the user
        message
            The message received from the MQTT broker
    """
    print("------------------------------------")
    print("MQTT Message Received at", datetime.datetime.now())
    print("Topic=",message.topic)
    print("qos=",message.qos)
   # print("message=", str(message.payload.decode("utf-8")))
    print("------------------------------------")
    
    if message.topic == "s_touch":
        light_id = lights[6] #I want to change light 0 (see diagram)
        
        data = int(message.payload.decode("utf-8")) #read data as int
        #I am expecting a 1 or 0
        new_color = (0, 0, 0) #If I receive data that is not 1 or 0, the light will turn white
        if data == 1:
            new_color = (0, 255, 0)
        elif data == 2:
            new_color = (255, 255, 0)
        elif data == 3:
            new_color = (255, 0 ,0)
        else:
            new_color = (255, 255 ,255)
        
        print("Turning light", light_id, "to color", new_color)
        
        # This sets an individual light
        nanoleaf_single.set_color(light_id, new_color)
    if message.topic == "weather_all":
   
        
        #light_id = lights[0] #I want to change light 0 (see diagram)
        message = message.payload #read data as string
        print(message)
        message = (encryption.decrypt(message))
        print(message)
        message = message.decode("utf-8")
        print(message)

        #Order is Temp, Humidity, Rain Fall, Wind Speed, Pressure, Wind Direction
        
        #Read in the message from MQTT, split it into an array at the commas
        my_list = message.split(",")
        print (my_list)
        #Disregard the Pi ID number, function, and location 
        my_list[0] = float(my_list[3])
        my_list[1] = float(my_list[4])
        my_list[2] = float(my_list[5])
                           

    #Temperature Light Control
        if 40 >= my_list[0]:
            nanoleaf_single.set_color(lights[0], (0,255,0))
             
        else :
            nanoleaf_single.set_color(lights[0], (255,0,0))
             

     #RAIN Light Control
        
        if my_list[1] >= 0:
            nanoleaf_single.set_color(lights[1], (0,255,0))
        else:
            nanoleaf_single.set_color(lights[1], (255,0,0))
     
    #Wind Speed Light Control
        if my_list[2] <= 15:
            nanoleaf_single.set_color(lights[2], (0,255,0))
        else :
            nanoleaf_single.set_color(lights[2], (255,0,0))
            
                    
        R = random.randint(0,255)
        G = random.randint(0,255)
        B = random.randint(0,255)
        nanoleaf_single.set_color(lights[3], (R,G,B))
        nanoleaf_single.set_color(lights[4], (R,G,B))
        nanoleaf_single.set_color(lights[5], (R,G,B))
        nanoleaf_single.set_color(lights[6], (R,G,B))
            
  
#         nanoleaf_single.set_color(lights[7], (40,40,40))
#         nanoleaf_single.set_color(lights[8], (40,40,40))
#         nanoleaf_single.set_color(lights[14], (40,40,40))
#         nanoleaf_single.set_color(lights[10], (40,40,40))
#         nanoleaf_single.set_color(lights[11], (40,40,40))

    #time.sleep(1)
    nanoleaf_single.sync()
   


# ----------------------------------------------
# Main client program
# ----------------------------------------------

# Creates an MQTT Client with a Sample Client ID
client = mqtt.Client(client_id="nano_demo_app")

# Connects to the MQTT Broker
client.connect("96.66.89.56")

# Tells the client what function to call when a message
# is received
client.on_message = on_message

# Publishes (i.e., sends) a message on a channel
# See MQTT documentation for Quality of Service (qos)
#client.publish("sensor", "hello world", qos=0)

# Subscribes to a Topic to Receive Messages

client.subscribe("weather_all", qos=0)





# Perpetually Listens for Messages on Subscribed Topics

client.loop_forever()

