"""Computes the estimate when a loop will be finished."""

__author__="Jesse Lord"
__date__="March 14, 2015"

import time

def timeInit():
    return time.time()

def extrapolateEnd(inittime,totaliter,index):
    current = time.time()
    secperiter = (current-inittime)/float(index)
    remainingsec = (totaliter-index)*secperiter
    return time.localtime(remainingsec+current)

def loopTiming(inittime,totaliter,index):
    if index == 1 or index == 2 or index == 10:
        endingtime = extrapolateEnd(inittime,totaliter,index)
        print "After,",index,"iteration(s) the loop expected to finish at",time.strftime('%X',endingtime),"on",time.strftime('%x',endingtime)
    if index == totaliter/2:
        endingtime = extrapolateEnd(inittime,totaliter,index)
        print "Halfway done. The loop expected to finish at",time.strftime('%X',endingtime),"on",time.strftime('%x',endingtime)
