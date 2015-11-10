# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 11:21:53 2015

@author: Ben Slabbert
"""


import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
        print "Connected with result code "+str(rc)
        client.subscribe('ben/spamming/send')


def on_message(client, userdata, msg):
        print 'message : ', str(msg.payload)


client = mqtt.Client()
#client.connect("192.168.97.1", 1883)
client.connect("192.168.123.1", port=1883)
client.on_connect = on_connect
client.on_message = on_message
count = 0

while 1:
        client.loop()
        print "Publish : ben/spamming/recieve " + str(count)
        client.publish("ben/spamming/recieve", payload=str(count), qos=0)
        count = count + 1
        time.sleep(0.25)
