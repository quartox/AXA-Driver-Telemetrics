"""Computes the regression analysis on the driver trip data."""

__author__="Jesse Lord"
__date__="March 12, 2015"

from features import computeFeatures
from readData import readData
import numpy as np
import sklearn.cluster as cluster
import sklearn.mixture as mix

def combineFeatures(features,driverindex,nfeatures,nsamples):
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
    return x


def combineClusters(y,nclusters,nsamples):
    DEBUG = False
    num_positive = nsamples/nclusters
    z1 = np.empty(0)
    z0 = np.empty(0)
    for ii in range(nclusters):
        (index,) = np.where(y == ii)
        if DEBUG:
            print ii,index.size
        if index.size >= num_positive:
            z1 = np.append(z1,index)
        else:
            z0 = np.append(z0,index)
    return (z0,z1)

def kmeans():
    drivers = readData()
    features = computeFeatures(drivers)
    nsamples = 200
    nfeatures = features[0][0].nfeatures

    x = combineFeatures(features,1,nfeatures,nsamples)

    nclusters = 5

    km = cluster.KMeans(n_clusters=nclusters,n_init=100,init='k-means++')
    y = km.fit_predict(x)

    (z0,z1) = combineClusters(y,nclusters,nsamples)
    return (z0,z1)
