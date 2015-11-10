import paho.mqtt.client as mqtt
import time
import glob
import os


while True:

	try:
		file_name = glob.glob('*output*.csv')[0] # any file called output in .csv format
		print file_name
	   
		if file_name != '':
			
			#####################################################
			def on_connect(client, userdata, flags, rc):
				print("Connected with result code "+str(rc))
				client.subscribe("file/recieved")
			#####################################################
			def on_message(client, userdata, msg):
			  print 'file recieved'
			  print str(msg.payload)
			  f = open('file_recieved.txt','w')
			  f.write('1')
			  f.close()
			#####################################################
			
		   
			client = mqtt.Client()
			#client.connect("146.232.171.44", port=1883)
			client.connect("192.168.123.1", 1883, 60)
				
			client.on_connect = on_connect
			client.on_message = on_message
			
			
			#f = open("C:\\Users\\Ben Slabbert\\Documents\\Varsity\\2015\\Thesis\\Python\\Big Brother\\data\\80.txt")
			
			flag = '0'
			count = 0
			while True:
				print 'sending file'
				f = open(file_name)
#				f = open('temp.txt')
				imagestring = f.read()
				byteArray = bytes(imagestring)
				print 'file published'
				client.publish("file/transfer", byteArray ,1)
				print '*************\nnum files sent : ', count,'\n******************\n'
				count += 1
				
				while flag != '1':
					print 'waiting for file to be recieved'
					f = open('file_recieved.txt','r')
					flag = f.read()
					f.close()
					client.loop()
					time.sleep(1)
				print 'file recieved, sending again'    
				f = open('file_recieved.txt','w')
				flag = f.write('0')
				f.close()
				break
	   
		# need to delete file transmitted
		os.system('sudo rm '+str(file_name))

	except:
		print 'no more files to transfer over mqtt'
		file_name = ''
		print 'sleeping, waiting for new files to transfer'
		time.sleep(10)
	

