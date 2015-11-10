# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 12:11:54 2015

@author: Ben Slabbert
"""

# this client will publish
# https://pypi.python.org/pypi/paho-mqtt

import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

client = mqtt.Client()

#client.connect("iot.eclipse.org", 1883)
#client.connect("192.168.97.1", 1883)
client.connect("192.168.123.1", port=1883)
client.on_connect = on_connect
#client.connect("localhost", port=1883)
#count = 0
#
#while 1:
#    print "Publish : ben/new " + str(count)
#    mqttc.publish("ben/new", payload=str(count), qos=0)
##    mqttc.publish("rpi/led/history", payload=byteArray, qos=0)
#    count = count + 1
#    time.sleep(1)

while 1:

    client.loop()
    f = open('C:\\Users\\Ben Slabbert\\Documents\\Varsity\\2015\\Thesis\\RPi\\led\\transmit_confirm.txt','r')
    line = f.read()
    f.close()
    print 'transmit ? ', line
    
    if line == '1':
        f = open('C:\\Users\\Ben Slabbert\\Documents\\Varsity\\2015\\Thesis\\RPi\\led\\set_led.txt','r')
        line = f.read() 
        f.close()
        line = line.split('.')
        line = line[0]
        print line 
        client.publish("led/control", payload=int(line), qos=1)

        
        trans_file = open('C:\\Users\\Ben Slabbert\\Documents\\Varsity\\2015\\Thesis\\RPi\\led\\transmit_confirm.txt','w')
        trans_file.write(str(0))
        trans_file.close()
    
    else:
        print 'no transmission'
    time.sleep(10)
    client.loop()
