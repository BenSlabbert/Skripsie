# http://iamtrask.github.io/2015/07/27/python-network-part2/

import numpy as np
import pickle
import time
from Drop_out_test_data import get_test_data

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

# compute sigmoid nonlinearity
def sigmoid(x):
    output = 1/(1+np.exp(-x))
    return output
# convert output of sigmoid function to its derivative

def sigmoid_output_to_derivative(output):
    return output*(1-output)


while 1:
    try:
        print '\n\n###################################\n\n\tNew Test\n\n###################################\n\n'
        tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst =  time.localtime()
        times, led_status = get_test_data(tm_hour)
           
        start = times[0]
        end = times[len(times)-1]+1  
        
        print 'Start time : ',start
        print 'End time : ',end
        X = load_obj('led_train_data_'+str(tm_hour)+'_'+str(tm_hour+1))[start:end]
#        X = np.vstack((X,X))
#        X = np.vstack((X,X))
#        X = np.vstack((X,X))
        X = np.vstack((X,load_obj('led_train_data_negative_'+str(tm_hour)+'_'+str(tm_hour+1))[start:end]))
    #    print X
        X_rows, X_cols = X.shape
        y = load_obj('led_train_labels_'+str(tm_hour)+'_'+str(tm_hour+1))
        
    #    print 'y',y
        
#        y = np.vstack((y,y))
#        y = np.vstack((y,y))
#        y = np.vstack((y,y))
        y = np.vstack((y,load_obj('led_train_labels_negative_'+str(tm_hour)+'_'+str(tm_hour+1))))
    #    print y
        y_rows, y_cols = y.shape
    #    print 'X shape : \n', X.shape
    #    print 'y shape : \n',y.shape
        alpha,hidden_dim,dropout_percent,do_dropout = (0.8,64,0.1,True)
        
        print "Training With Alpha:" + str(alpha)
        np.random.seed(1)
        
        # randomly initialize our weights with mean 0
        synapse_0 = 2*np.random.random((X_cols,hidden_dim)) - 1
        synapse_1 = 2*np.random.random((hidden_dim,1)) - 1
        
        for j in xrange(60000):
        
            # Feed forward through layers 0, 1, and 2    
            layer_0 = X
            layer_1 = sigmoid(np.dot(layer_0,synapse_0))
            
            if(do_dropout):
                layer_1 *= np.random.binomial([np.ones((len(X),hidden_dim))],1-dropout_percent)[0] * (1.0/(1-dropout_percent))
                
            layer_2 = sigmoid(np.dot(layer_1,synapse_1))
            
            # how much did we miss the target value?
            layer_2_error = y - layer_2
            
            if (j% 10000) == 0:
                print "Error after "+str(j)+" iterations:" + str(np.mean(np.abs(layer_2_error)))
            
            # in what direction is the target value?
            # were we really sure? if so, don't change too much.
            layer_2_delta = layer_2_error*sigmoid_output_to_derivative(layer_2)
            
            # how much did each l1 value contribute to the l2 error (according to the weights)?
            layer_1_error = layer_2_delta.dot(synapse_1.T)
            
            # in what direction is the target l1?
            # were we really sure? if so, don't change too much.
            layer_1_delta = layer_1_error * sigmoid_output_to_derivative(layer_1)
            
            synapse_1 += alpha * (layer_1.T.dot(layer_2_delta))
            synapse_0 += alpha * (layer_0.T.dot(layer_1_delta))
        
        
        
        test = led_status
        print test.shape
        print 'train data :\n',X
        print 'test data : \n',test
        #for i in xrange(len(led_status)-1):
        #    test[i] = np.round(np.random.rand(),0)
    
        layer_0 = test
        layer_1 = sigmoid(np.dot(layer_0,synapse_0))
        layer_2 = sigmoid(np.dot(layer_1,synapse_1))
        print 'prediction : \n', np.round(layer_2,4)
        print 'current value : ',test[end-start-1]
        print 'desired value : ',X[0][end-start-1]
        
        info = np.log2((1)/(np.round(layer_2,4)))
        
#        if np.round(layer_2,4) < 0.6:
#            
#            f = open('transmit_confirm.txt','w')
#            f.write(str(1))
#            f.close()
#            
#            print 'set led to : ', X[0][end-start-1]
#            f = open('set_led.txt','w')
#            f.write(str(X[0][end-start-1]))
#            f.close()
#            
#        else:
#            print 'led status is acceptable'
#            f = open('transmit_confirm.txt','w')
#            f.write(str(0))
#            f.close()
        print '\ninfo ',info[0]
        print '\n'
        print 'sleeping now'   
        
        info_file = open('drop_out_info_network_activity.txt','a')
        info_file.write(str(info[0])+','+str(tm_hour + (tm_min+0.0)/(60.0))+'\n')        
        info_file.close()
        
        time.sleep(60)
    except Exception,e: 
        print 'ERROR:\n',str(e)
        time.sleep(10)
