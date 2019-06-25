from __future__ import division
from __future__ import print_function

import numpy as np
import math as m
import sys


#  Call the new, IMU-corrected LCF file 1
lcfIMU = sys.argv[1]
#  Call the old, GPS-based LCF file 2
lcfGPS = sys.argv[2]
#  Call up the BIL header file for metadata
hdrFile = sys.argv[3]
bilFile = sys.argv[4]

time_imu = [] 
pitch_imu = [] 
roll_imu = [] 
yaw_imu = [] 
lat_imu = [] 
lon_imu = [] 
alt_imu = []
fourth_imu = []
third_imu = []
second_imu = []
first_imu = []

time_gps = [] 
pitch_gps = [] 
roll_gps = [] 
yaw_gps = [] 
lat_gps = [] 
lon_gps = [] 
alt_gps = []
fourth_gps = []
third_gps = []
second_gps = []
first_gps = []

with open(lcfIMU) as infile:
	#  Read each column from LCF and append to lists
	for line in infile:
		#  Time
		time_imu.append(float(line.split(',')[0]))
		#  Pitch
		pitch_imu.append(float(line.split(',')[1]))
		#  Roll
		roll_imu.append(float(line.split(',')[2]))
		#  Yaw
		yaw_imu.append(float(line.split(',')[3]))
		#  Latitude
		lat_imu.append(float(line.split(',')[4]))
		#  Longitude
		lon_imu.append(float(line.split(',')[5]))
		#  Altitude
		alt_imu.append(float(line.split(',')[6]))
		fourth_imu.append(int(line.split(',')[7]))
		third_imu.append(int(line.split(',')[8]))
		second_imu.append(int(line.split(',')[9]))
		first_imu.append(int(line.split(',')[10]))	

#  Cast into arrays to allow operations
#    Units:    
#	pitch, roll, yaw = radians
#	latitude, longitude = decimal degrees
#	altitude = meters
time_imu = np.asarray(time_imu)
pitch_imu = np.asarray(pitch_imu)
roll_imu = np.asarray(roll_imu)
yaw_imu = np.asarray(yaw_imu)
lat_imu = np.asarray(lat_imu)
lon_imu = np.asarray(lon_imu)
alt_imu = np.asarray(alt_imu)

with open(lcfGPS) as infile:
	for line in infile:
		#  Time
		time_gps.append(float(line.split()[0]))
		#  Pitch
		pitch_gps.append(float(line.split()[1]))
		#  Roll
		roll_gps.append(float(line.split()[2]))
		#  Yaw
		yaw_gps.append(float(line.split()[3]))
		#  Latitude
		lat_gps.append(float(line.split()[4]))
		#  Longitude
		lon_gps.append(float(line.split()[5]))
		#  Altitude
		alt_gps.append(float(line.split()[6]))
		fourth_gps.append(int(line.split()[7]))
		third_gps.append(int(line.split()[8]))
		second_gps.append(int(line.split()[9]))
		first_gps.append(int(line.split()[10]))	

time_gps = np.asarray(time_gps)
pitch_gps = np.asarray(pitch_gps)
roll_gps = np.asarray(roll_gps)
yaw_gps = np.asarray(yaw_gps)
lat_gps = np.asarray(lat_gps)
lon_gps = np.asarray(lon_gps)
alt_gps = np.asarray(alt_gps)

nLineScans = len(time_gps)

#  Read from the header file for the number of samples 
#  which is the number of pixels per line scan
with open(hdrFile, 'r') as f:
	for line in f:
		if 'samples' in line:
			nPixelsPerLineScan = int(line.split(' = ')[1])

earthRadius = 6371000 #meters
d2r = m.pi/180.0
r2d = 180.0/m.pi

#  Define the field of view (geometrically related to swath width) in each direction
#    fovPara is the bearing (direction of flight)
#    fovPerp is perpendicular to bearing (line scan direction)
fovPara = 0.109 * d2r
fovPerp = 33.0 * d2r

#  Initialize lists for pixel dimensions per line scan
pixelWidth_meter = []
pixelLength_meter = []
pixelWidth_deg = []
pixelLength_deg = []
#  Initialize lists for difference between GPS and IMU tajectories
diff_lat_deg = []
diff_lon_deg = []
diff_lat_meters = []
diff_lon_meters = []
pixelShift = []

#  Calculate pixel ground resolution (decimal degrees per pixel)
for i in range(nLineScans):
	#  Calculate swath width at flight height (meters)
	swathWidth = 2.0 * alt_gps[i] * m.tan(fovPerp / 2.0)

	#  Uniformly divide into number of samples (pixels per line scan)
	pixelWidth_meter.append(swathWidth / nPixelsPerLineScan)
	pixelWidth_deg.append((pixelWidth_meter[i] / earthRadius) * r2d)

	#  Calculate swath length at flight height (meters)
	swathLength = 2.0 * alt_gps[i] * m.tan(fovPara / 2.0)

	#  Pushbroom sensor is 1 pixel in the parallel direction
	pixelLength_meter.append(swathLength / 1)	
	pixelLength_deg.append((pixelLength_meter[i] / earthRadius) * r2d)

	#  Calculate the difference between the centers of the GPS and IMU point-of-views
	#  and cast it as an integer (= number of pixels in shift per line scan)
	diff_lat_deg.append((lat_gps[i] - lat_imu[i]) * d2r)
	diff_lon_deg.append((lon_gps[i] - lon_imu[i]) * d2r)

	#  Convert difference to meters for reference to pixel width calculated above
	diff_lat_meters.append(diff_lat_deg[i] * earthRadius)
	diff_lon_meters.append(diff_lon_deg[i] * earthRadius)

	#  Calculate the number of pixels per line scan shift
	#  ceiling function yields integer (note: discrete nature of pixels)
	pixelShift.append(int(m.ceil(diff_lon_meters[i]/ pixelWidth_meter[i])))

maxShift = max(pixelShift)
minShift = min(pixelShift)

#  Create bounding box large enough to contain the GPS and IMU trajectories
lat_box_min = min([min(lat_gps), min(lat_imu)])
lat_box_max = max([max(lat_gps), max(lat_imu)])

lon_box_min = min([min(lon_gps), min(lon_imu)])
lon_box_max = max([max(lon_gps), max(lon_imu)])

#  Define amount of buffer to add to each dimension (~ integer multiples of pixel dimension)
lat_buffer = (0.5*nPixelsPerLineScan + maxShift) * pixelLength_deg[0]
lon_buffer = (0.5*nPixelsPerLineScan + maxShift) * pixelWidth_deg[0]

#  Define bounding box vertices through min/max of GPS & IMU coordinates and buffer, respecting direction
boxV1 = np.asarray([lat_box_min - lat_buffer, lon_box_min - lon_buffer])
boxV2 = np.asarray([lat_box_max + lat_buffer, lon_box_min - lon_buffer])
boxV3 = np.asarray([lat_box_max + lat_buffer, lon_box_max + lon_buffer])
boxV4 = np.asarray([lat_box_min - lat_buffer, lon_box_max + lon_buffer])
#print(boxV1, boxV2, boxV3, boxV4)

#  Calculate bounding box edge lengths
#boxE1 = m.sqrt((boxV1[1] - boxV2[1])**2 + (boxV1[0] - boxV2[0])**2)
#boxE2 = m.sqrt((boxV4[1] - boxV1[1])**2 + (boxV4[0] - boxV1[0])**2)
#print(boxE1, boxE2)

#  Translate the edge lengths into number of pixels
nPixel1 = int(m.ceil(m.sqrt((boxV1[1] - boxV2[1])**2 + (boxV1[0] - boxV2[0])**2) / pixelWidth_deg[0]))
nPixel2 = int(m.ceil(m.sqrt((boxV2[1] - boxV3[1])**2 + (boxV2[0] - boxV3[0])**2) / pixelWidth_deg[0]))
#nPixel3 = int(m.ceil(m.sqrt((boxV3[1] - boxV4[1])**2 + (boxV3[0] - boxV4[0])**2) / pixelWidth_deg[0]))
#nPixel4 = int(m.ceil(m.sqrt((boxV4[1] - boxV1[1])**2 + (boxV4[0] - boxV1[0])**2) / pixelWidth_deg[0]))
#print(nPixel1, nPixel2, nPixel3, nPixel4)

box = np.zeros((nPixel1, nPixel2))
#print(box.shape)


import spectral.io.envi as envi

#  Open ENVI-formatted header file and BIL binary
img = envi.open(hdrFile, bilFile)
img = img.load()
img = np.asarray(img)
#LineScans = img.shape[0]
#nPixelsPerLineScan = img.shape[1]
#print(img.shape)

#  Choose the starting point in the placeholder (box) array for the trajectory
start_traj = [int(box.shape[0] / 4), int(box.shape[1] / 2)]
#print(start_traj)

for i in range(img.shape[0]):
	for j in range(-int(img.shape[1] / 2), int(img.shape[1] / 2)):
		box[start_traj[0] + i , start_traj[1] + j + pixelShift[i]] = img[i, j, 0]

#for i in range(nLineScans):
#	box[i, :]

#print(box[start_traj[0]:start_traj[0]+100,start_traj[1]:start_traj[1]+100])

np.savetxt('array.csv', box, delimiter=",")

#from matplotlib import pyplot as plt
#plt.imshow(box, interpolation = 'nearest')
#plt.show()

from scipy.misc import toimage
toimage(box).show()


import csv
from itertools import izip
 	
with open('pixelShift.csv', 'w') as output:
	writer = csv.writer(output)
	writer.writerows(izip(pixelShift, diff_lat_meters, diff_lon_meters, pixelLength_meter, pixelWidth_meter))


