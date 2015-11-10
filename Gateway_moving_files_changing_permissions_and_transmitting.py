# -*- coding: utf-8 -*-
"""
Created on Mon May 11 21:25:30 2015

@author: root
"""

import glob
import numpy as np
import shutil
import os
import time

# get list of files in directory
list_of_files = glob.glob("/tshark/*.cap")

while True:
    if len(list_of_files) > 1: # must always have more than 1 file in the directory
        
        print '. . . enough files to continue. . . '
        
        list_of_files = sorted(list_of_files) # sort the list (old first)
	file_directory = list_of_files[0] # getting the oldest file
	print 'converting file from : \n', file_directory
        # getting the file name
        file_name = file_directory.split('/') 
        file_name = file_name[len(file_name)-1]
	print 'file name : \n',file_name
        # use tshark to create a .csv file from the .cap data
        os.system('sudo tshark -r '+file_directory+' -T fields -e frame.time -e tcp.srcport -e tcp.dstport -e eth.src -e eth.dst -e ip.src -e ip.dst -e ip.proto -E separator=, -E header=y -E quote=d > '+file_name[:-4]+'.csv')
        # need to move this file to new directory
	shutil.move(file_name[:-4]+'.csv', '/home/pi/project/mqtt/')
	os.system('sudo rm '+file_directory)

    else:
    	print 'not enough files'
	print 'sleeping....' 
	time.sleep(10)
    time.sleep(1)

    list_of_files = glob.glob("/tshark/*.cap") # update list of files in directory
