"""Tests how close a variable is to Gaussian."""

__author__="Jesse Lord"
__date__="March 12, 2015"

import scipy.stats as stats
import numpy as np
import math

def computeMoments(x):
    """Computes the third and fourth central moments of the distribution."""
    return (abs(stats.skew(x)),abs(stats.kurtosis(x,None,True)))


def checkMin(oldskew,oldkurt,newskew,newkurt,oldtransform,newtransform):
    """Determines if previous minimum skew and/or kurtosis should be replaced."""
    if (newskew < oldskew and newkurt < oldkurt) or (newkurt < oldkurt and (newskew-oldskew) < 2.0*(oldkurt-newkurt) ):
        return (newskew,newkurt,newtransform)
    elif newskew < oldskew:
        return (oldskew,oldkurt,oldtransform)
    elif newkurt < oldkurt:
        return (oldskew,oldkurt,oldtransform)
    else:
        return (oldskew,oldkurt,oldtransform)


def powerLaw(minskew,minkurt,transform,x):
    """Computes a power law transformation of the data."""
    exponent = 0.05
    while exponent < 20:
        y = x**exponent
        (newskew,newkurt) = computeMoments(y)
        (minskew,minkurt,transform) = checkMin(minskew,minkurt,newskew,newkurt,transform,exponent)
        exponent *= 1.5
    #endwhile
    return (minskew,minkurt,transform)


def finalTransform(minskew,minkurt,transform,newx,x):
    goalskew = 2.0
    goalkurt = 1.0
    if minskew < goalskew and minkurt < goalkurt:
        if transform == 0:
            values = x
        elif transform > 0:
            values = x**transform
        elif transform == -1:
            values = np.log(x)
        elif transform == -2:
            values = np.exp(x)
        if newx is None:
            returnarray = np.empty((1,values.size))
            returnarray[0,:] = values
        else:
            oldshape = newx.shape
            nfeatures = oldshape[0]+1
            nexamples = oldshape[1]
            returnarray = np.empty((nfeatures,nexamples))
            returnarray[:nfeatures-1,:] = newx
            returnarray[-1,:] = values
    #endif minskew < goalskew and minkurt < goalkurt
    else:
        returnarray = newx
    return returnarray


def gaussianDistribution(x,nfeatures,nexamples):
    minskew = np.empty(nfeatures)
    minkurt = np.empty(nfeatures)
    transform = np.zeros(nfeatures)
    newx = None
    for ii in range(nfeatures):
        (minskew[ii],minkurt[ii]) = computeMoments(x[ii,:])
        # checking different power law transformations
        (minskew[ii],minkurt[ii],transform[ii]) = powerLaw(minskew[ii],minkurt[ii],transform[ii],x[ii,:])
        # checking logarithmic transformation
        y = np.log(x[ii,:])
        (newskew,newkurt) = computeMoments(y)
        (minskew[ii],minkurt[ii],transform[ii]) = checkMin(minskew[ii],minkurt[ii],newskew,newkurt,transform[ii],-1)
        # checking exponential transformation
        y = np.exp(x[ii,:])
        (newskew,newkurt) = computeMoments(y)
        (minskew[ii],minkurt[ii],transform[ii]) = checkMin(minskew[ii],minkurt[ii],newskew,newkurt,transform[ii],-2)
        newx = finalTransform(minskew[ii],minkurt[ii],transform[ii],newx,x[ii,:])
    #endfor
    return newx
