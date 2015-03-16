"""Writes the submission."""

__author__="Jesse Lord"
__date__="March 13, 2015"

import numpy as np
from kmeans import kmeans
from regression import svm
import processData
import readData
import csv
import loopTiming

if __name__ == "__main__":
    with open('submission.csv','wb') as f:
        submission = csv.writer(f)
        (ndrivers,directory_names) = readData.allDrivers()
        finaldrivers = False
        neg = readData.readNegativeExamples(directory_names,finaldrivers)
        (xneg,featuremax) = processData.computeNegFeatures(neg)
        inittime = loopTiming.timeInit()
        for index in range(ndrivers):
            loopTiming.loopTiming(inittime,ndrivers,index)
            if index == ndrivers-5:
                finaldrivers = True
                neg = readData.readNegativeExamples(directory_names,finaldrivers)
                (xneg,featuremax) = processData.computeNegFeatures(neg)
            driver = readData.readData(index,directory_names)
            (x,nfeatures) = processData.processData(driver,featuremax)
            (x,z0,z1,nsamples) = kmeans(x)
            prob = svm(x,xneg,z0,z1,nsamples,nfeatures)
            probmax = np.amax(prob)
            probmin = np.amin(prob)
            #if probmax < 0.8 or probmin > 0.2:
            #    print "Max and min probability",probmax,probmin,"for index",index
            for ii in range(nsamples):
                submission.writerow([str(index+1)+'_'+str(ii+1),prob[ii]])
