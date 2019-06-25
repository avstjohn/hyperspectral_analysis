from __future__ import division
from __future__ import print_function

import numpy as np
import math as m
from itertools import izip
import csv
import sys


#  Call the GPS-based LCF file
lcfFile = sys.argv[1]
#  Call up the BIL header file for metadata
hdrFile = sys.argv[2]
bilFile = sys.argv[3]

00_read_original_LCF(lcfFile)

earthRadius = 6371000 #meters
d2r = m.pi/180.0
r2d = 180.0/m.pi

01_calculate_IMU_trajectory(altitude, roll, latitude, longitude, nLineScans, earthRadius)

with open('new_LCF.csv', 'w') as outfile:
	writer = csv.writer(outfile)
	writer.writerows(izip(time, pitch, roll, yaw, correctedLat, correctedLon, altitude, fourth, third, second, first))

infile = 'new_LCF.csv'
02_read_new_LCF(infile)

#  Read from the header file for the number of samples 
#  which is the number of pixels per line scan
with open(hdrFile, 'r') as f:
	for line in f:
		if 'samples' in line:
			nPixelsPerLineScan = int(line.split(' = ')[1])

#  Define the field of view (geometrically related to swath width) in each direction
#    fovPara is the bearing (direction of flight)
#    fovPerp is perpendicular to bearing (line scan direction)
fovPara = 0.109 * d2r
fovPerp = 33.0 * d2r

03_calculate_pixel_shift(nLineScans, nPixelsPerLineScan, alt_gps, fovPara, fovPerp, earthRadius)

04_create_bounding_box()
# output array (bounding box) with placeholder values: '1' for occupied, '0' for unoccupied

#  Apply pixel shift to each line scan
05_populate_trajectory()

#  Recreate image with geometric corrections (with transparency channel)
output_image()



