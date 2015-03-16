"""Uses kmeans to compute which trips are the primary driver compared to any other drivers."""

__author__="Jesse Lord"
__date__="March 12, 2015"

from readData import readData
import numpy as np
import sklearn.cluster as cluster
import sklearn.mixture as mix

def combineClusters(y,nclusters,nsamples):
    DEBUG = False
    num_positive = nsamples/nclusters
    z0 = np.empty(0)
    z1 = np.empty(0)
    for ii in range(nclusters):
        (index,) = np.where(y == ii)
        if DEBUG:
            print ii,index.size
        if index.size >= num_positive:
            z1 = np.append(z1,index)
        else:
            z0 = np.append(z0,index)
    z0 = z0.astype(int)
    z1 = z1.astype(int)
    return (z0,z1)


def kmeans(x):

    nsamples = 200

    nclusters = 5

    km = cluster.KMeans(n_clusters=nclusters,n_init=20,init='k-means++')
    y = km.fit_predict(x)

    (z0,z1) = combineClusters(y,nclusters,nsamples)
    # randomly shuffling the indeces
    np.random.shuffle(z0)
    np.random.shuffle(z1)
    return (x,z0,z1,nsamples)
