import sys

import numpy as np
def normalizer(fin):
    themin = np.amin(fin,axis = 0)
    themax = np.amax(fin,axis = 0)
    mean = np.mean(fin,axis = 0)
    std = np.std(fin,axis =0)
    length = len(themin)
    for i in range(length):
        themin[i] = mean[i] - std[i]
        themax[i] = mean[i] + std[i]

    for i in range(len(fin)):
        cur = fin[i]
  
        for j in range(len(cur)):
            fin[i][j] = (fin[i][j] - themin[j]) / (themax[j] - themin[j])
    
    return(fin)
    
    

    
    
    
        

