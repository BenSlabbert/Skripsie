# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 13:19:58 2015

@author: Ben Slabbert
"""
# this client will subscribe
# https://pypi.python.org/pypi/paho-mqtt

import paho.mqtt.client as mqtt
import time
import numpy as np

tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst =  time.localtime()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

    client.subscribe("ben/LED_status")
    client.subscribe("ben/light_intensity")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst =  time.localtime()
    print(str(tm_hour)+':'+str(tm_min)+':'+str(tm_sec)+' \t|| '+msg.topic+" "+str(msg.payload))    
    if msg.topic == 'ben/LED_status':
        f = open("LED_status_"+str(tm_hour)+".txt", 'a')
        t = tm_min
        f.write(str(msg.payload)+','+str(t)+'\n')
        f.close()
            
    if msg.topic == 'ben/light_intensity':
        f = open("light_intensity_"+str(tm_hour)+".txt", 'a')
        t = tm_min
        f.write(str(msg.payload)+','+str(t)+'\n')
        f.close()
        
     
    
            
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
#client.connect("192.168.97.1", port=1883)
#client.connect("192.168.224.1", 1883, 60)
#client.connect("iot.eclipse.org", 1883, 60)
#client.connect("146.232.171.44", 1883, 60)
client.connect("192.168.123.1", 1883, 60)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
