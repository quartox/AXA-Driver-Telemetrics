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

def numberOfDrivers():
    directory_names = list(glob.glob(os.path.join(DATA_PATH,"driver-telemetrics/","*")))
    return len(directory_names)

def readData():
    """Find all of the folders that represent all of the drivers in the data set."""
    filepath = os.path.join(DATA_PATH,"driver-telemetrics/","*")
    directory_names = list(glob.glob(filepath))
    num_drivers = len(directory_names)
    num_chars = len(filepath)-1 # the number of characters before the wildcard
    drivers = list()
    for folder in directory_names:
        current_driver = Driver(int(folder[num_chars:]))
        (current_driver.x,current_driver.y) = readDriver(folder)
        drivers.append(current_driver)
    return drivers

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
