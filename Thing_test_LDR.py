import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

GPIO.setmode(GPIO.BCM)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(23,GPIO.IN)

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe("led/control")

def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))
	if int(msg.payload) == 1:
		GPIO.output(7,GPIO.HIGH)
	if int(msg.payload) == 0:
		GPIO.output(7,GPIO.LOW)

def RCtime(PiPin):
	measurement = 0
	GPIO.setup(PiPin,GPIO.OUT)
	GPIO.output(PiPin,GPIO.LOW)
	time.sleep(0.1)

	GPIO.setup(PiPin,GPIO.IN)
	while (GPIO.input(PiPin) == GPIO.LOW):
		measurement += 1

	return measurement

client = mqtt.Client()	
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.123.1", port=1883)

tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst =  time.localtime()

wait_time = 60 - tm_sec
time.sleep(wait_time)
while 1:
	client.loop()
	light_intensity = str(RCtime(25))

	if int(light_intensity) > 5000:
		GPIO.output(7,GPIO.HIGH)
	if int(light_intensity) < 5000:
		GPIO.output(7,GPIO.LOW) 

	LED = GPIO.input(23)

	print "Light intensity : ", light_intensity
	print 'LED status : ', LED
	client.publish("ben/LED_status", payload=LED, qos=0)
	client.publish("ben/light_intensity", payload=light_intensity, qos=0)
	tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst =  time.localtime()
	temp = tm_min
	while temp == tm_min:
		client.loop()
		time.sleep(1)
		tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst =  time.localtime()
