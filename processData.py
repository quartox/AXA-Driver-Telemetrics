"""Uses kmeans to compute which trips are the primary driver compared to any other drivers."""

__author__="Jesse Lord"
__date__="March 14, 2015"

from features import computeFeatures
import numpy as np

def combineFeatures(features,driverindex,featuremax,nfeatures,nsamples):
    x = np.empty((nsamples,nfeatures))
    for ii in range(nsamples):
        x[ii,0] = features[driverindex][ii].max_separation
        x[ii,1] = features[driverindex][ii].final_distance
        x[ii,2] = features[driverindex][ii].total_time
        x[ii,3] = features[driverindex][ii].max_vel
        x[ii,4] = features[driverindex][ii].mean_vel
        x[ii,5] = features[driverindex][ii].max_accel
        x[ii,6] = features[driverindex][ii].mean_accel
        x[ii,7] = features[driverindex][ii].max_jerk
        x[ii,8] = features[driverindex][ii].mean_jerk
    for ii in range(nfeatures):
        x[:,ii] /= featuremax[ii]
    return x

def combineNegativeFeatures(features,numdrivers,nfeatures,nsamples):
    x = np.empty((nsamples*numdrivers,nfeatures))
    for ii in range(nsamples):
        for jj in range(numdrivers):
            x[ii+nsamples*jj,0] = features[jj][ii].max_separation
            x[ii+nsamples*jj,1] = features[jj][ii].final_distance
            x[ii+nsamples*jj,2] = features[jj][ii].total_time
            x[ii+nsamples*jj,3] = features[jj][ii].max_vel
            x[ii+nsamples*jj,4] = features[jj][ii].mean_vel
            x[ii+nsamples*jj,5] = features[jj][ii].max_accel
            x[ii+nsamples*jj,6] = features[jj][ii].mean_accel
            x[ii+nsamples*jj,7] = features[jj][ii].max_jerk
            x[ii+nsamples*jj,8] = features[jj][ii].mean_jerk
    featuremax = np.empty(nfeatures)
    for ii in range(nfeatures):
        featuremax[ii] = np.amax(x[:,ii])*1.01
        x[:,ii] /= featuremax[ii]
    return (x,featuremax)

def computeNegFeatures(neg):
    features = computeFeatures(neg)
    nsamples = 200
    nfeatures = features[0][0].nfeatures
    numdrivers = len(features)
    (x,featuremax) = combineNegativeFeatures(features,numdrivers,nfeatures,nsamples)
    return (x,featuremax)

def processData(drivers,featuremax):
    features = computeFeatures(drivers)
    nsamples = 200
    nfeatures = features[0][0].nfeatures
    x = combineFeatures(features,0,featuremax,nfeatures,nsamples)
    return (x,nfeatures)
