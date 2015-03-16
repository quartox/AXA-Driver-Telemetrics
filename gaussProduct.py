"""Computes the regression analysis on the driver trip data."""

__author__="Jesse Lord"
__date__="March 12, 2015"

from features import computeFeatures
from readData import readData
import plotData
import numpy as np
import math
from gaussianDistribution import gaussianDistribution

def Gaussian(x,mu,sigma):
    return np.exp(-(((x-mu) / sigma)**2)/2.0) / (math.sqrt(2.0*math.pi)*sigma)

if __name__ == "__main__":
    drivers = readData()
    features = computeFeatures(drivers)
    nn = 200
    nfeatures = features[0][0].nfeatures
    x = np.empty((nfeatures,nn))
    for ii in range(nn):
        x[0,ii] = features[0][ii].max_separation
        x[1,ii] = features[0][ii].final_distance
        x[2,ii] = features[0][ii].total_time
        x[3,ii] = features[0][ii].max_vel
        x[4,ii] = features[0][ii].mean_vel
        x[5,ii] = features[0][ii].max_accel
        x[6,ii] = features[0][ii].mean_accel
        x[7,ii] = features[0][ii].max_jerk
        x[8,ii] = features[0][ii].mean_jerk
    xgauss = gaussianDistribution(x,nfeatures,nn)
    ngauss = xgauss.shape[0]
    mu = np.empty(ngauss)
    sigma = np.empty(ngauss)
    for ii in range(ngauss):
        mu[ii] = np.mean(xgauss[ii,:])
        sigma[ii] = np.std(xgauss[ii,:])
    prob = np.empty(nn)
    a = Gaussian(xgauss[:,ii],mu,sigma)
    print xgauss[:,0]
    print mu
    print sigma
    print a
    for ii in range(nn):
        prob[ii] = np.prod(Gaussian(xgauss[:,ii],mu,sigma))
    #import matplotlib.pyplot as p
    #p.plot(prob)
    #p.show()
    print np.min(prob),np.max(prob)
