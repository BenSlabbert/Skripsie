# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 11:23:25 2015

@author: Ben Slabbert
"""

import numpy as np
from sklearn.neural_network import BernoulliRBM
from sklearn.pipeline import Pipeline
from sklearn import linear_model, metrics


###############################################################################
import pickle

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

###############################################################################

def rbm(test):

    X = [0,0,0,0.99944475,0,0,0,0,1,0,0]
    X = np.vstack((X,X))
    X = np.vstack((X,X))
    X = np.vstack((X,X))
    X = np.vstack((X,[1,1,1,0,1,1,1,1,0,1,1]))
    X = np.vstack((X,[0,0,0,0,1,0.06,0.02,0.3,0.5,0.5,0.7]))
    X = np.vstack((X,[0,0,0,0,1,0.1,0.1,0.3,0.5,0.5,0.7]))
    X = np.vstack((X,[0,0.3,0,0.7,0,0,0,0.2,0.8,0,0.3]))
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
    y = np.vstack((y,[0]))
#    print y
    y_rows, y_cols = y.shape
    
    X_train = X
    Y_train = y
    
    X_test = test
    Y_test = np.array([0])
#    
#    print 'X_train\n',X_train
#    print X_train.shape
#    print 'Y_train\n',Y_train
#    print Y_train.shape
#    print 'X_test\n',X_test
#    print 'Y_test\n',Y_test
    
    # Models we will use
    logistic = linear_model.LogisticRegression()
    rbm = BernoulliRBM(random_state=0, verbose=True)
    
    classifier = Pipeline(steps=[('rbm', rbm), ('logistic', logistic)])
    
    ###############################################################################
    # Training
    
    # Hyper-parameters. These were set by cross-validation,
    # using a GridSearchCV. Here we are not performing cross-validation to
    # save time.
    rbm.learning_rate = 0.9
    rbm.n_iter = 5
    # More components tend to give better prediction performance, but larger fitting time
    rbm.n_components = 20
    logistic.C = 6000.0
    
    # Training RBM-Logistic Pipeline
    classifier.fit(X_train, Y_train)
    
    # Training Logistic regression
    logistic_classifier = linear_model.LogisticRegression(C=100.0)
    logistic_classifier.fit(X_train, Y_train)
    
    ###############################################################################
    # Evaluation
    
#    print("Logistic regression using RBM features:\n%s\n" % (
#        metrics.classification_report(
#            Y_test,
#            classifier.predict(X_test))))
    
#    print("Logistic regression using raw pixel features:\n%s\n" % (
#        metrics.classification_report(
#            Y_test,
#            logistic_classifier.predict(X_test))))
    
#    print 'classes : ',classifier.classes_
#    print 'RBM and Logistic regression : ', classifier.predict(X_test) 
#    print 'Raw Logistic regression', logistic_classifier.predict(X_test)
    
    logistic_proba = logistic_classifier.predict_proba(X_test)
    print 'logistic_proba',logistic_proba
    
#    print 'logistic_classifier decision function : \n',logistic_classifier.decision_function(X_test)
#    print 'logistic_classifier predict_proba : \n', logistic_proba
    
    classifier_proba = classifier.predict_proba(X_test)
    print 'classifier_proba',classifier_proba
    
#    print 'classifier decision function : \n',classifier.decision_function(X_test)
#    print 'classifier decision predict_proba : \n',classifier_proba
#    print X[0]
#    print test
    print 'classes : ',classifier.classes_

    return np.log2((1)/(np.round(logistic_proba[0][1],4))), np.log2((1)/(np.round(classifier_proba[0][1],4)))
#
#NN_test_data = np.array([ [0,0,0,1,0,0,0,0,1,0,0] ])
#logistic_info, classifier_info = rbm(np.array(np.ndarray.tolist(NN_test_data)))
#
#print 'Logistic classifier information generated : \t', logistic_info
#print 'rbm classifier information generated : \t', classifier_info
