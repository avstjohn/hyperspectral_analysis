from __future__ import division
from __future__ import print_function

import numpy as np
import scipy.misc as sm
import matplotlib.cm as cm
from PIL import Image
import math
from itertools import izip
import csv
import sys
import spectral.io.envi as envi


lcfFile = sys.argv[1]
hdrFile = sys.argv[2]
bilFile = sys.argv[3]
fileIndex = int(sys.argv[4])

#  Open ENVI-formatted header file and BIL binary
bil = envi.open(hdrFile, bilFile)
#bil = bil.load()
#bil = np.asarray(bil)

time = [] 
pitch = [] 
roll = [] 
yaw = [] 
latitude = [] 
longitude = [] 
altitude = []
fourth = []
third = []
second = []
first = []

with open(lcfFile) as infile:
	#  Read each column from LCF and append to lists
	for line in infile:
		#  Time
		time.append(float(line.split()[0]))
		#  Pitch
		pitch.append(float(line.split()[1]))
		#  Roll
		roll.append(float(line.split()[2]))
		#  Yaw
		yaw.append(float(line.split()[3]))
		#  Latitude
		latitude.append(float(line.split()[4]))
		#  Longitude
		longitude.append(float(line.split()[5]))
		#  Altitude
		altitude.append(float(line.split()[6]))
		#  4th to last
		fourth.append(int(line.split()[7]))
		#  3rd to last
		third.append(int(line.split()[8]))
		#  2nd to last
		second.append(int(line.split()[9]))
		#  1st to last
		first.append(int(line.split()[10]))	

#  Cast into arrays to allow operations
#    Units:    
#	pitch, roll, yaw = radians
#	latitude, longitude = decimal degrees
#	altitude = meters
time = np.asarray(time)
pitch = np.asarray(pitch)
roll = np.asarray(roll)
yaw = np.asarray(yaw)
latitude = np.asarray(latitude)
longitude = np.asarray(longitude)
altitude = np.asarray(altitude)

nLineScans = len(time)

earthRadius = 6378137 #meters
d2r = math.pi/180.0
r2d = 180.0/math.pi


correctedLat = []
correctedLon = []

for i in range(nLineScans):
	#  Approximate great-circle arc from actual GPS location to FOV location due to the roll angle	
	arcLength = altitude[i] * math.tan(roll[i])

	#  Note that atan2 chooses the correct quadrant and returns values in radians 	
	deltaLat = (arcLength / earthRadius) * math.sin(math.atan2(arcLength, earthRadius))
	deltaLon = (arcLength / earthRadius) * math.cos(math.atan2(arcLength, earthRadius))

	#  corrected (latitude, longitude) in the "roll angle reference frame"
	correctedLat.append(latitude[i] + deltaLat * r2d)
	correctedLon.append(longitude[i] + deltaLon * r2d)	

with open('imu-trajectory.csv', 'w') as output:
	writer = csv.writer(output)
	writer.writerows(izip(time, pitch, roll, yaw, correctedLat, correctedLon, altitude, fourth, third, second, first))










