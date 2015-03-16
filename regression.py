"""Computes the regression analysis on the driver trip data using the kmeans identified trips as the labeled data sets."""

__author__="Jesse Lord"
__date__="March 13, 2015"

import numpy as np
from sklearn.svm import SVC

trainingset = 0.7

def svmGaussKernel(x,y,C,gamma,prob):
    """Computes the classification boundary using a gaussian kernel."""
    # To compute the gaussian kernel use the gamma function with
    # gamma = 1 / (2 sigma^2)
    clf = SVC(C=C,kernel='rbf',gamma=gamma,probability=prob,class_weight='auto')
    clf.fit(x,y)
    return clf

def selectTrainSet(x,xneg,z0,z1,nsamples,nfeatures):
    """Divides the data into training set and validation set."""
    # permanent negative examples
    numperm = xneg.shape[0]
    iiperm = np.arange(numperm)
    np.random.shuffle(iiperm)
    ntrainperm = round(trainingset*numperm)
    nvalperm = numperm-ntrainperm
    iitrainperm = iiperm[:ntrainperm]
    iivalperm = iiperm[ntrainperm:]
    # the number of negative trip examples identified by the kmeans clustering
    numpos = z1.size
    numneg = z0.size
    trainpos = int(round(trainingset*numpos))
    trainneg = int(round(trainingset*numneg))
    valpos = numpos-trainpos
    # initializing training set and validation set
    ntrain = trainpos+trainneg
    nvalidation = nsamples-ntrain
    xtrain = np.empty((ntrain+ntrainperm,nfeatures))
    xval = np.empty((nvalidation+nvalperm,nfeatures))
    xtrain[:trainpos,:] = x[z1[:trainpos],:]
    xtrain[trainpos:ntrain,:] = x[z0[:trainneg],:]
    xval[:valpos,:] = x[z1[trainpos:],:]
    xval[valpos:nvalidation,:] = x[z0[trainneg:],:]
    # adding the permanently negative examples
    xtrain[ntrain:,:] = xneg[iitrainperm,:]
    xval[nvalidation:,:] = xneg[iivalperm,:]
    # the classification of the training and validation set
    ytrain = np.zeros(ntrain+ntrainperm)
    yval = np.zeros(nvalidation+nvalperm)
    ytrain[:trainpos] = 1
    yval[:valpos] = 1
    return (xtrain,ytrain,xval,yval)

def validation(x,y,xcv,ycv):
    """Determines the best choice of regularization and gaussian parameters on cross validation set."""
    # loop through a range of regularization and gaussian parameters
    bestParams = np.zeros(3)
    besttrainpred = 0.0
    C = 1.0e0
    Cmax = 1.1e0
    gamma_init = 8.0e3
    gammamax = 8.1e3
    bestParams[1] = C
    bestParams[2] = gamma_init
    delta = 2.0
    prob = False
    Debug = False
    while C < Cmax:
        gamma = gamma_init
        while gamma < gammamax:
            clf = svmGaussKernel(x,y,C,gamma,prob)
            # determining how well this fit predicts the cross validation data
            pcv = clf.predict(xcv)
            prediction = np.mean(pcv==ycv)
            if Debug:
                p = clf.predict(x)
                trainprediction = np.mean(p==y)
                print prediction
                print np.min(xcv),np.max(xcv)
                print np.min(x),np.max(x)
                print pcv.shape,np.min(pcv),np.max(pcv)
                print p.shape,np.min(p),np.max(p)
                print trainprediction
                print C,gamma
                print ycv
                print pcv
                exit()
            if np.amin(pcv) != np.amax(pcv) and prediction > bestParams[0]:
                bestParams[0] = prediction
                bestParams[1] = C
                bestParams[2] = gamma
            # increase the parameters by a factor of delta
            gamma *= delta
        # endwhile gamma < gammamax
        C *= delta
    # endwhile C < Cmax
    #print "Best Prediction",bestParams[0]
    # computing the fit with the best fit parameters
    C = bestParams[1]
    gamma = bestParams[2]
    return (C,gamma)

def probability(x,y,C,gamma,xcv):
    prob = True
    clf = svmGaussKernel(x,y,C,gamma,prob)
    trainprob = clf.predict_proba(x)
    valprob = clf.predict_proba(xcv)
    Debug = False
    if Debug:
        print C,gamma
        p = clf.predict(x)
        prediction = np.mean(p==y)
        print prediction
        (pos,) = np.where(y==1)
        (neg,) = np.where(y==0)
        print pos.shape,neg.shape
        print np.amax(trainprob[pos][1]),np.amin(trainprob[pos][1])
        print np.amax(trainprob[neg][1]),np.amin(trainprob[neg][1])
    nt = trainprob.shape[0]
    tprob = np.empty(nt)
    for ii in range(nt):
        tprob[ii] = trainprob[ii][1]
    nv = valprob.shape[0]
    vprob = np.empty(nv)
    for ii in range(nv):
        vprob[ii] = valprob[ii][1]
    return (tprob,vprob)

def combineProb(z0,z1,nsamples,trainprob,valprob):
    prob = np.empty(nsamples)
    numpos = z1.size
    numneg = z0.size
    trainpos = int(round(trainingset*numpos))
    trainneg = int(round(trainingset*numneg))
    valpos = numpos-trainpos
    prob[z1[:trainpos]] = trainprob[:trainpos]
    prob[z0[:trainneg]] = trainprob[trainpos:]
    prob[z1[trainpos:]] = valprob[:valpos]
    prob[z0[trainneg:]] = valprob[valpos:]
    return prob

def svm(x,xneg,z0,z1,nsamples,nfeatures):
    (xtrain,ytrain,xval,yval) = selectTrainSet(x,xneg,z0,z1,nsamples,nfeatures)
    (C,gamma) = validation(xtrain,ytrain,xval,yval)
    #print "C and gamma",C,gamma
    (trainprob,valprob) = probability(xtrain,ytrain,C,gamma,xval)
    prob = combineProb(z0,z1,nsamples,trainprob,valprob)
    return prob
