# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 11:23:24 2015

@author: Ben Slabbert
"""

import numpy as np
from sklearn.mixture import GMM
import  matplotlib.pyplot as plt
from collections import Counter
import copy
###############################################################################
import pickle

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

###############################################################################


def best_gmm(test):
        M_best = load_obj('calls_per_hour')   
        logprob, responsibilities =  M_best.score_samples(test)
        information = (np.log2(1/np.exp(logprob[0])))
        return information
        
