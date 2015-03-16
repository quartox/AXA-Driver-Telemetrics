"""Read in the driver telemetric data for the AXA Kaggle competition."""

__author__="Jesse Lord"
__date__="March 10, 2015"

import glob
import os
import csv
from driver import Driver

DATA_PATH = "/home/Jesse/Programming/Kaggle/data/"

if __name__ == "__main__":
    filepath = os.path.join(DATA_PATH,"driver-telemetrics/","*")
    directory_names = list(glob.glob(filepath))
    num_drivers = len(directory_names)
    num_chars = len(filepath)-1 # the number of characters before the wildcard
    for folder in directory_names:
        driver = Driver(int(folder[num_chars:]))
        allx = list(list())
        ally = list(list())
        file_names = os.listdir(folder)
        for file in file_names:
            with open(os.path.join(folder,file),'rb') as f:
                csvfile = csv.reader(f)
                csvfile.next()
                x = list()
                y = list()
                for row in csvfile:
                    x.append(row[0])
                    y.append(row[1])
            allx.append(x)
            ally.append(y)
        driver.x = allx
        driver.y = ally
        print len(driver.x),len(driver.y)
        exit()

def allDrivers():
    filepath = os.path.join(DATA_PATH,"driver-telemetrics/","*")
    directory_names = list(glob.glob(filepath))
    num_drivers = len(directory_names)
    return (num_drivers,directory_names)

def readDriver(folder):
    """Read data for a single driver."""
    allx = list(list())
    ally = list(list())
    file_names = os.listdir(folder)
    for file in file_names:
        with open(os.path.join(folder,file),'rb') as f:
            csvfile = csv.reader(f)
            csvfile.next()
            x = list()
            y = list()
            for row in csvfile:
                x.append(float(row[0]))
                y.append(float(row[1]))
        allx.append(x)
        ally.append(y)
    return (allx,ally)

def readData(index,directory_names):
    """Find all of the folders that represent all of the drivers in the data set."""
    filepath = os.path.join(DATA_PATH,"driver-telemetrics/")
    num_chars = len(filepath) # the number of characters before the wildcard
    drivers = list()
    folder = directory_names[index]
    current_driver = Driver(int(folder[num_chars:]))
    (current_driver.x,current_driver.y) = readDriver(folder)
    drivers.append(current_driver)
    return drivers

def readNegativeExamples(directory_names,finaldrivers):
    """Find all of the folders that represent all of the drivers in the data set."""
    filepath = os.path.join(DATA_PATH,"driver-telemetrics/")
    num_drivers = len(directory_names)
    num_chars = len(filepath) # the number of characters before the wildcard
    drivers = list()
    if finaldrivers:
        iirange = range(5)
    else:
        iirange = range(num_drivers-5,num_drivers)
    for ii in iirange:
        folder = directory_names[ii]
        current_driver = Driver(int(folder[num_chars:]))
        (current_driver.x,current_driver.y) = readDriver(folder)
        drivers.append(current_driver)
    return drivers
