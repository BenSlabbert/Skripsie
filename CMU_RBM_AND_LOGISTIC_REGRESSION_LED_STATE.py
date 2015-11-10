# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 11:23:25 2015

@author: Ben Slabbert
"""

import numpy as np
from sklearn.neural_network import BernoulliRBM
from sklearn.pipeline import Pipeline
from sklearn import linear_model, metrics
from Drop_out_test_data import get_test_data
import time

###############################################################################
import pickle

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

###############################################################################
while 1:
    try:
        print '\n\n###################################\n\n\tNew Test\n\n###################################\n\n'
        tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst =  time.localtime()
        # training + test data
        times, led_status = get_test_data(tm_hour)
        
        print times
        print led_status
           
        start = times[0]
        end = times[len(times)-1]+1
        print start
        print end
        X = load_obj('led_train_data_'+str(tm_hour)+'_'+str(tm_hour+1))[start:end]
        X = np.vstack((X,X))
#        X = np.vstack((X,X))
#        X = np.vstack((X,X))
        X = np.vstack((X,load_obj('led_train_data_negative_'+str(tm_hour)+'_'+str(tm_hour+1))[start:end]))
#       print X
        X_rows, X_cols = X.shape
        y = load_obj('led_train_labels_'+str(tm_hour)+'_'+str(tm_hour+1))
        
        #    print 'y',y
        
        y = np.vstack((y,y))
#        y = np.vstack((y,y))
#        y = np.vstack((y,y))
        y = np.vstack((y,load_obj('led_train_labels_negative_'+str(tm_hour)+'_'+str(tm_hour+1))))
        #    print y
        y_rows, y_cols = y.shape
        
        X_train = X
        Y_train = y
        
        X_test = led_status
        Y_test = np.array([0])
        
        print 'X_train\n',X_train
        #print X_train.shape
        print 'Y_train\n',Y_train
        #print Y_train.shape
        print 'X_test\n',X_test
        print 'Y_test\n',Y_test
        
        # Models we will use
        logistic = linear_model.LogisticRegression()
        rbm = BernoulliRBM(random_state=0, verbose=True)
        
        classifier = Pipeline(steps=[('rbm', rbm), ('logistic', logistic)])
        
        ###############################################################################
        # Training
        
        # Hyper-parameters. These were set by cross-validation,
        # using a GridSearchCV. Here we are not performing cross-validation to
        # save time.
        rbm.learning_rate = 0.8
        rbm.n_iter = 5
        # More components tend to give better prediction performance, but larger fitting time
        rbm.n_components = 50
        logistic.C = 6000.0
        
        # Training RBM-Logistic Pipeline
        classifier.fit(X_train, Y_train)
        
        # Training Logistic regression
        logistic_classifier = linear_model.LogisticRegression(C=100.0)
        logistic_classifier.fit(X_train, Y_train)
        
        ###############################################################################
        # Evaluation
        
        print("Logistic regression using RBM features:\n%s\n" % (
            metrics.classification_report(
                Y_test,
                classifier.predict(X_test))))
        
        print("Logistic regression using raw pixel features:\n%s\n" % (
            metrics.classification_report(
                Y_test,
                logistic_classifier.predict(X_test))))
        
        print 'classes : ',classifier.classes_
        print 'RBM and Logistic regression : ', classifier.predict(X_test) 
        print 'Raw Logistic regression', logistic_classifier.predict(X_test)
        
        logistic_proba = logistic_classifier.predict_proba(X_test)
        
        print 'logistic_classifier decision function : \n',logistic_classifier.decision_function(X_test)
        print 'logistic_classifier predict_proba : \n', logistic_proba
        
        classifier_proba = classifier.predict_proba(X_test)
        
        print 'classifier decision function : \n',classifier.decision_function(X_test)
        print 'classifier decision predict_proba : \n',classifier_proba
        
        
        if classifier_proba[0][1] < 0.6:
            print 'classifier ___________ led is acting strange'
            print 'current value : ',led_status[end-start-1]
            print 'desired value : ',X[0][end-start-1]
            
            f = open('transmit_confirm.txt','w')
            f.write(str(1))
            f.close()
            
            print 'set led to : ', X[0][end-start-1]
            f = open('set_led.txt','w')
            f.write(str(X[0][end-start-1]))
            f.close()
            
        if logistic_proba[0][1] < 0.6:
            print 'logistic _______________ led is acting strange'
            print 'current value : ',led_status[end-start-1]
            print 'desired value : ',X[0][end-start-1]
        
        
        print 'information \n\nlogistic : ',np.log2((1)/(np.round(logistic_proba[0][1],4)))
        print 'classifier : ',np.log2((1)/(np.round(classifier_proba[0][1],4)))
        
        info_file = open('classifier_info_network_activity.txt','a')
        info_file.write(str(np.log2((1)/(np.round(classifier_proba[0][1],4))))+','+str(tm_hour + (tm_min+0.0)/(60.0))+'\n')        
        info_file.close()     
        
        info_file = open('logistic_info_network_activity.txt','a')
        info_file.write(str(np.log2((1)/(np.round(logistic_proba[0][1],4))))+','+str(tm_hour + (tm_min+0.0)/(60.0))+'\n')        
        info_file.close()  
        
        
        
        print '\n\nsleeping'
        time.sleep(60)
    

    except Exception,e: 
        print 'ERROR:\n',str(e)
        time.sleep(10)


