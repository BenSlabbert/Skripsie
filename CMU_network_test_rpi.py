# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 13:16:21 2015

@author: Ben Slabbert
"""

import numpy as np
from collections import Counter
from network_test_rpi_drop_out import drop_out
from network_test_rpi_rbm_and_logistic_regression import rbm
from get_best_fit_gmm import best_gmm
import time
import smtplib

old_count = 0
new_count = 100

def email(msg):
    try:
        tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst =  time.localtime()
        fromaddr = 'benraspberrypi@gmail.com'
        toaddrs  = ['benjamin.slabbert@gmail.com']
        
        message = 'Subject: %s\n\n%s' % ('Network Test Results : ' + str(tm_year)+'/'+str(tm_mon)+'/'+str(tm_mday) +' '+ str(tm_hour)+':'+str(tm_min)+':'+str(tm_sec), msg)
            
        # Credentials (if needed)
        username = 'benraspberrypi'
        password = 'r45pb3rryp1'
        
        # The actual mail send
        print 'setting up server'
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        print 'logging in to server'
        server.login(username,password)
        print 'sending mail'
        server.sendmail(fromaddr, toaddrs, message)
        print 'mail sent, quitting'
        server.quit()
    except:
        print 'no internet connection'
        pass
    return

while 1:
    # get latest data file
    f = open('C:\\Users\\Ben Slabbert\\Documents\\Varsity\\2015\\Thesis\\Python\\Python MQTT\\count.txt', 'r')
    old_count = new_count
    new_count = int(f.read())-1
    print new_count
    f.close()
    
    if old_count != new_count:   
    
        try:    
            f = open('C:\\Users\\Ben Slabbert\\Documents\\Varsity\\2015\\Thesis\\Python\\Python MQTT\\temp_'+str(new_count)+'.csv', 'rb')
            print 'working on temp_',str(new_count)
            temp = f.readline()
            data = []
            temp = np.array(f.readline().replace('"','').replace('\r','').replace('\n','').split(','))
    #        print temp
            data = temp
            print data
            while temp[0] != '':
                try:
                    if temp[2] != '' or temp[3] != '':
                        data  = np.vstack((data,temp))
                except:
                    pass
                temp = np.array(f.readline().replace('"','').replace('\r','').replace('\n','').split(','))    
            f.close()
        
            
            rows,cols = data.shape
    #        print rows
            start_time = data[0][1].split(' ')[2].split(':')
            end_time = data[rows-1][1].split(' ')[2].split(':')
            
            start_time = float(start_time[0]) + float(start_time[1])/60.0 + float(start_time[2])/3600.0
            end_time = float(end_time[0]) + float(end_time[1])/60.0 + float(end_time[2])/3600.0
    
            if end_time < start_time:
                end_time += 24.0
            
            print start_time
            print end_time
            print data[0]
            ports = data[:,2]
            counter = Counter(data[:,2])
            print 'number of calls : ', rows
            print 'number of ports used', len(counter.items())
            print 'calls per hour : ',rows/(end_time-start_time)
            
            
            # gmm for calls per hour
            #M_best = best_gmm([rows,rows,rows,rows,rows,rows,rows,rows,rows,rows,rows], 2, 2, 'calls_per_hour')
            # NN ports used
            """                            Features Data Format
                    #################################################################################################################################################
                    # data[0] || data[1] || data[2] || data[3] || data[4] ||   data[5]   ||   data[6]   ||    data[7]  ||   data[8]   ||   data[9]   ||  data[10]   #
                    # --------||---------||---------||---------||---------||------------ ||-------------||-------------||-------------||-------------||------------ #
            port no.#    22   ||   80    ||   443   ||  1883   || 0-10000 || 10000-20000 || 20000-30000 || 30000-40000 || 40000-50000 || 50000-60000 || 60000-70000 #
                    #################################################################################################################################################
            """
            NN_test_data = np.zeros((1, 11))
            for i in xrange(rows):
                flag = 0
                try:
                    if int(ports[i]) == 22:
                        NN_test_data[0][0] += 1
                        flag = 1
                        
                    if int(ports[i]) == 80:
                        NN_test_data[0][1] += 1
                        flag = 1
                        
                    if int(ports[i]) == 443:
                        NN_test_data[0][2] += 1
                        flag = 1
                        
                    if int(ports[i]) == 1883:
                        NN_test_data[0][3] += 1
                        flag = 1
                        
                    if 0 < int(ports[i]) < 10000 and flag == 0:
                        NN_test_data[0][4] += 1
                        
                    if 10000 < int(ports[i]) < 20000:
                        NN_test_data[0][5] += 1
                        
                    if 20000 < int(ports[i]) < 30000:
                        NN_test_data[0][6] += 1
                        
                    if 30000 < int(ports[i]) < 40000:
                        NN_test_data[0][7] += 1
                        
                    if 40000 < int(ports[i]) < 50000:
                        NN_test_data[0][8] += 1
                        
                    if 50000 < int(ports[i]) < 60000:
                        NN_test_data[0][9] += 1
                        
                    if 60000 < int(ports[i]) < 70000:
                        NN_test_data[0][10] += 1
                except:
                    print ports[i]
                    pass
                    
            NN_test_data = NN_test_data/np.max(NN_test_data)
            print NN_test_data
            #NN_test_data = np.array([ [0.6,0,0,0,0.2,0.6,0.3,1,0.6,1,1] ])
            
            
            NN_info_threshold = 0.737
            gmm_info_threshold = 10.0
            
            # call RBM
            logistic_info, classifier_info = rbm(np.array(np.ndarray.tolist(NN_test_data)))
            # call NN
            drop_out_info = drop_out(np.array(np.ndarray.tolist(NN_test_data)))
            # call gmm
            call_per_hour = [rows/(end_time-start_time)]
            gmm_info = best_gmm(call_per_hour)
            #gmm_info = best_gmm(2000)
            gmm_file = open('call_per_hour_info.txt','a')
            gmm_file.write(str(gmm_info)+'\n')
            gmm_file.close()
            
            email_message = ''
            
            print '\n\n###################################\n\n'
            email_message = email_message + '\n\n###################################\n\n'
            print 'testing for fit : \n'
            email_message = email_message + '\ntesting for fit : \n'
            print 'RBM and NN fits : \n'
            email_message = email_message + '\nRBM and NN fits : \n'
            print 'Logistic classifier information generated : \t', logistic_info
            email_message = email_message + '\nLogistic classifier information generated : \t' +  str(logistic_info)
            print 'rbm classifier information generated : \t', classifier_info
            email_message = email_message + '\nrbm classifier information generated : \t\t' +  str(classifier_info)
            print 'drop out information generated : \t\t', drop_out_info[0][0]
            email_message = email_message + '\ndrop out information generated : \t\t' +  str(drop_out_info[0][0])
            print '\ncall per hour from test data : \t', call_per_hour[0]
            email_message = email_message + '\ncall per hour from test data : \t' +  str(call_per_hour[0])
            print '\ninformation generated from calls per hour : \n', gmm_info
            email_message = email_message + '\ninformation generated from calls per hour : \n' +  str(gmm_info)
            print '\nthe data set fits ?\n'
            email_message = email_message + '\n\nthe data set fits ?\n'
            
            if logistic_info < NN_info_threshold:
                print 'logistic \taccepts'
                email_message = email_message + '\nlogistic \taccepts'
            else:
                print 'logistic \twarns'
                email_message = email_message + '\nlogistic \twarns'
            
            if classifier_info < NN_info_threshold:
                print 'classifier \taccepts'
                email_message = email_message + '\nclassifier \taccepts'
            else:
                print 'classifier \twarns'
                email_message = email_message + '\nclassifier \twarns'
            
            if drop_out_info < NN_info_threshold:
                print 'drop out \taccepts'
                email_message = email_message + '\ndrop out \taccepts'
            else:
                print 'drop out \twarns'
                email_message = email_message + '\ndrop out \twarns'
                
            if gmm_info < gmm_info_threshold:
                print 'gmm \taccepts calls per hour'
                email_message = email_message + '\ngmm \taccepts calls per hour'
            else:
                print 'gmm \twarns calls per hour '
                email_message = email_message + '\ngmm \twarns calls per hour '
            
            print '\n\n###################################\n\n'
            email_message = email_message + '\n\n\n###################################\n\n'
            
            print '\nSENDING EMAIL\n'
#            email(email_message)
            time.sleep(30)
        except:
            print 'file not ready'
            print 'sleeping'
            time.sleep(30)
            pass
    else:
        print 'file already examined'
        time.sleep(30)

