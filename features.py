"""The features of each trip for the regression."""

__author__="Jesse Lord"
__date__="March 10, 2015"

from math import sqrt
from readData import readData

class Features:
    def __init__(self,id):
        self.id = id
        self.nfeatures = 9
        # initializing the features for the classification
        self.max_separation = None
        self.final_distance = 0.0
        self.total_time = 0.0
        self.max_vel = None
        self.mean_vel = 0.0
        self.max_accel = None
        self.mean_accel = 0.0
        self.max_jerk = None
        self.mean_jerk = 0.0

def distance(x0,y0,x1,y1):
    """Computes the Euclidian distance between two points."""
    return sqrt((x1-x0)**2 + (y1-y0)**2)

def computeAccel(xm1,x0,xp1):
    """Computes the acceleration using a second order centered finite difference derivative. Implicitely assumes that the change in time is one second, otherwise the derivative would include a division by (delta_time)**2."""
    return (xm1 - 2.0*x0 + xp1)

def computeJerk(xm2,xm1,x0,xp1,xp2):
    """Computes the jerk using a second order centered finite difference derivative. Implicitely assumes that the change in time is one second, otherwise the derivative would include a division by (delta_time)**3."""
    return (-0.5*xm2+xm1-xp1+0.5*xp2)

def derivatives(x5,y5):
    """Computes the acceleration and jerk using numerical derivatives. Uses the inputs of the format: xm2 is x position 2 seconds ago, xm1 is x position 1 second ago, x0 is the current x position, xp1 is x position in 1 second, and xp2 is the x position in 2 seconds. Same format for the y positions."""
    xaccel = computeAccel(x5[1],x5[2],x5[3])
    yaccel = computeAccel(y5[1],y5[2],y5[3])
    accel = sqrt(xaccel**2 + yaccel**2)
    xjerk = computeJerk(x5[0],x5[1],x5[2],x5[3],x5[4])
    yjerk = computeJerk(y5[0],y5[1],y5[2],y5[3],y5[4])
    jerk = sqrt(xjerk**2 + yjerk**2)
    return( accel, jerk )

def distances_and_derivs(trip,x,y):
    """Computes the distance and derivatives (i.e. velocity, acceleration, jerk) based on the position data for each trip."""
    num_seconds = len(x)
    trip.total_time = num_seconds
    for ii in range(1,num_seconds):
        # the distance traveled since the previous second
        dist = distance(x[ii-1],y[ii-1],x[ii],y[ii])
        trip.mean_vel += dist/num_seconds
        if trip.max_vel is None or trip.max_vel < dist:
            trip.max_vel = dist
        # the distance from the origin, i.e. x[0] and y[0]
        origin_dist = distance(x[0],y[0],x[ii],y[ii])
        if trip.max_separation is None or trip.max_separation < origin_dist:
            trip.max_separation = origin_dist
        if ii == num_seconds-1:
            trip.final_distance = origin_dist
        # the derivatives, i.e. acceleration and jerk
        if ii > 1 and ii < num_seconds-2:
            # the five position cooridnates needed to compute the derivatives
            x5 = [x[ii-2],x[ii-1],x[ii],x[ii+1],x[ii+2]]
            y5 = [y[ii-2],y[ii-1],y[ii],y[ii+1],y[ii+2]]
            (accel, jerk) = derivatives(x5,y5)
            trip.mean_accel += accel/(num_seconds-4)
            if trip.max_accel is None or trip.max_accel < accel:
                trip.max_accel = accel
            trip.mean_jerk += jerk/(num_seconds-4)
            if trip.max_jerk is None or trip.max_jerk < jerk:
                trip.max_jerk = jerk

def computeFeatures(drivers):
    """Computes the features from the driver telemetric data."""
#if __name__ == "__main__":
    features = list()
    for driver in drivers:
        driver_features = list()
        num_trips = len(driver.x)
        for ii in range(num_trips):
            x = driver.x[ii]
            y = driver.y[ii]
            trip = Features(driver.id)
            distances_and_derivs(trip,x,y)
            driver_features.append(trip)
        features.append(driver_features)
    return features
