# http://iamtrask.github.io/2015/07/27/python-network-part2/

import numpy as np
import pickle
import time


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

def drop_out(test):
    
    X = [0,0,0,0.99944475,0,0,0,0,1,0,0]
    X = np.vstack((X,X))
    X = np.vstack((X,X))
    X = np.vstack((X,X))
    X = np.vstack((X,[1,1,1,0,1,1,1,1,0,1,1]))
    X = np.vstack((X,[0,0,0,0,1,0.06,0.02,0.3,0.5,0.5,0.7]))
    X = np.vstack((X,[1,0,0,1,0,0,0,0.02,0.98,0,0]))
#    print X
    X_rows, X_cols = X.shape
    y = [1]
    
#    print 'y',y
    
    y = np.vstack((y,y))
    y = np.vstack((y,y))
    y = np.vstack((y,y))
    y = np.vstack((y,[0]))
    y = np.vstack((y,[0]))
    y = np.vstack((y,[0]))
#    print y
    y_rows, y_cols = y.shape
#    print 'X shape : \n', X.shape
#    print 'y shape : \n',y.shape
    alpha,hidden_dim,dropout_percent,do_dropout = (0.8,64,0.1,True)
    
#    print "Training With Alpha:" + str(alpha)
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
    
    
    

#    print test.shape
#    print 'train data :\n',X[0]
#    print 'test data : \n',test
    #for i in xrange(len(led_status)-1):
    #    test[i] = np.round(np.random.rand(),0)

    layer_0 = test
    layer_1 = sigmoid(np.dot(layer_0,synapse_0))
    layer_2 = sigmoid(np.dot(layer_1,synapse_1))
    print 'prediction : \n', np.round(layer_2,4)

    
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
#    print 'info ',info
    
    return info
#NN_test_data = np.array([ [0,0,0,0.95,0,0,0,0,1,0,0] ])
#drop_out_info = drop_out(np.array(np.ndarray.tolist(NN_test_data)))
#print 'drop out information generated : \t\t', drop_out_info[0][0]
