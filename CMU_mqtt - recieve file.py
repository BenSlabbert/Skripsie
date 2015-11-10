# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 13:12:44 2015

@author: Ben Slabbert
"""

import time
import paho.mqtt.client as mqtt
#####################################################
def set_connect_flag():
    f = open('connect_flag.txt','w')
    f.write('1')
    f.close()
    return
#####################################################    
def get_connect_flag():
    f = open('connect_flag.txt','r')
    flag = str(f.read())
    f.close()
    return flag
#####################################################    
def reset_connect_flag():
    f = open('connect_flag.txt','w')
    f.write('0')
    f.close()
    return
#####################################################
def on_connect(client, userdata, flags, rc):
    set_connect_flag()
    print("Connected with result code "+str(rc))
    client.subscribe("file/transfer")
    client.subscribe("$SYS/broker/clients/active")
    client.publish('file_transfer/ready',payload=1,qos=2)
#####################################################
def on_message(client, userdata, msg):
        
    if str(msg.topic) == 'file/transfer':
      tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst =  time.localtime()
      print str(tm_hour)+':'+str(tm_min)+':'+str(tm_sec)+ '\t|| file recieved'
      client.publish('file/recieved', payload=1)
      
      f = open('count.txt', 'r')
      cnt = int(f.readline())
      print cnt
      f.close()
      
      f = open('count.txt', 'w')
      f.write(str(cnt+1))
      f.close()
      
      with open('temp_'+str(cnt)+'.csv', 'w') as fd:
          f = str(msg.payload)
          fd.write(f)
          fd.close()
#####################################################      
      
client = mqtt.Client()
#client.connect("192.168.97.1", 1883)
#client.connect("146.232.171.44", port=1883)
client.connect("192.168.123.1", port=1883)

client.on_connect = on_connect
client.on_message = on_message
flag = get_connect_flag()

while flag != '1':
    print 'waiting for connction'
    client.loop()
    time.sleep(0.025)
    flag = get_connect_flag()
    
print 'connected'
reset_connect_flag()

while True:
    client.loop()







