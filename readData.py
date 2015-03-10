"""Read in the driver telemetric data for the AXA Kaggle competition."""

__author__="Jesse Lord"
__date__="March 10, 2015"

import glob
import os
import csv

DATA_PATH = "/home/Jesse/Programming/Kaggle/data/Driver_telemetric/"

if __name__ == "__main__":
    directory_names = list(glob.glob(os.path.join(DATA_PATH,"train","*")))
    num_classes = len(directory_names)
    for folder in directory_names:
        file_names = os.listdir(folder)
        with open(os.path.join(folder,file_names[0]),'rb') as f:
            file = csv.reader(f)
            file.next()
            for row in file:
                x = row[0]
                y = row[1]

def numberOfClasses():
    directory_names = list(glob.glob(os.path.join(DATA_PATH,"train","*")))
    return len(directory_names)

def readDriver():
    directory_names = list(glob.glob(os.path.join(DATA_PATH,"train","*")))
    num_classes = len(directory_names)
