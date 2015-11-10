import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
	print "Connected with result code "+str(rc)
	client.subscribe('ben/spamming/recieve')


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
    	print "Publish : ben/spamming/send " + str(count)
	client.publish("ben/spamming/send", payload=str(count), qos=0)
    	count = count + 1
    	time.sleep(0.25)

