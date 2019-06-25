'''
distance = []
for i in range(nLineScans):
	lat = latitude[i]
	lon = longitude[i]

	diffArcLength = altitude[i] * np.tan(roll[i] * d2r)

	latFOV = diffArcLength * np.cos(math.atan2(diffArcLength, earthRadius)) * r2d
	lonFOV = diffArcLength * np.sin(math.atan2(diffArcLength, earthRadius)) * r2d

	deltaLat = lat - latFOV
	deltaLon = lon - lonFOV

	#  Haversine formula to calculate the great-circle distance between two points
	a = np.sin(0.5 * deltaLat * d2r)**2 + np.cos(lat * d2r) * np.cos(latFOV * d2r) * np.sin(0.5 * deltaLon * d2r)**2
	c = 2.0 * math.atan2(np.sqrt(a), np.sqrt(1.0 - a))
	D = earthRadius * c

	distance.append(D)

	#correctedLat.append(latitude[i] + deltaLat)
	#correctedLon.append(longitude[i] + deltaLon)

	with open('test1.csv', 'w') as output:
		writer = csv.writer(output)
		writer.writerows(izip(latitude, longitude, distance))
'''	


'''
HAVERSINE
for i in range(1, nLineScans):
	lat1 = latitude[i-1]
	lat2 = latitude[i]
	lon1 = longitude[i-1]
	lon2 = longitude[i]

	deltaLat = lat2 - lat1
	deltaLon = lon2 - lon1
	
	#  Haversine formula to calculate the great-circle distance between two points
	a = np.sin(0.5 * deltaLat * d2r)**2 + np.cos(lat1 * d2r) * np.cos(lat2 * d2r) * np.sin(0.5 * deltaLon * d2r)**2
	c = 2.0 * math.atan2(np.sqrt(a), np.sqrt(1.0 - a))
	D = earthRadius * c

	distance.append(D)

	#  Calculate bearing as great-circle arc is followed
	arg1 = np.sin(deltaLat * d2r) * np.cos(lon2 * d2r)
	arg2 = np.cos(lon1 * d2r) * np.sin(lon2 * d2r) - np.sin(lon1 * d2r) * np.cos(lon2 * d2r) * np.cos(deltaLat * d2r)
	directionOfTravel = math.atan2(arg1, arg2)

	bearing.append(directionOfTravel * r2d)
	
	#  Convert (latitude, longitude) to (x, y) of the GPS location
	xGPS.append(earthRadius * np.cos(lat1 * d2r) * np.cos(lon1 * d2r))
	yGPS.append(earthRadius * np.cos(lat1 * d2r) * np.sin(lon1 * d2r))	

	#  Add corrections to GPS location due to roll
	xFOV.append(xGPS[i-1] + altitude[i-1] * np.tan(roll[i-1] * d2r) * np.cos(bearing[i-1] * d2r))
	yFOV.append(yGPS[i-1] + altitude[i-1] * np.tan(roll[i-1] * d2r) * np.sin(bearing[i-1] * d2r))

	#  Convert back to (corrected) latitude and longitude
#	correctedLat = math.asin(altitude[i-1] / earthRadius)
#	correctedLon = math.atan2(yGPS[i-1], xGPS[i-1])  

with open('test.csv', 'w') as output:
	writer = csv.writer(output)
	writer.writerows(izip(latitude, longitude, xGPS, yGPS, bearing, distance, xFOV, yFOV))
'''
#  Write out to CSV with corrected latitude and longitude values
#correctedLCF = 'correctedTestLCF.csv'
#with open(correctedLCF, 'w') as output:
#	writer = csv.writer(output)
#	writer.writerows(izip(time, pitch, roll, yaw, correctedLat, correctedLong, altitude, fourth, third, second, first))





'''
CRAP, PROBABLY
magnitudeGPS = np.sqrt(latitude**2 + longitude**2)
magnitudeFOV = magnitudeGPS - altitude * np.tan(roll*(math.pi/180.0))

correction = np.abs(magnitudeGPS - magnitudeFOV)

directionGPS = longitude / latitude
directionFOV = (-1.0) * directionGPS

latCorrection = correction * np.cos(directionFOV*(math.pi/180.0))
longCorrection = correction * np.sin(directionFOV*(math.pi/180.0))

correctedLat = latitude + latCorrection
correctedLong = longitude + longCorrection 

#  Cast back into lists
time = np.array(time).tolist()
pitch = np.array(pitch).tolist()
roll = np.array(roll).tolist()
yaw = np.array(yaw).tolist()
correctedLat = np.array(correctedLat).tolist()
correctedLong = np.array(correctedLong).tolist()
altitude = np.array(altitude).tolist()

#  Write out to CSV with corrected latitude and longitude values
correctedLCF = 'correctedTestLCF.csv'
with open(correctedLCF, 'w') as output:
	writer = csv.writer(output)
	writer.writerows(izip(time, pitch, roll, yaw, correctedLat, correctedLong, altitude, fourth, third, second, first))




swathWidth = 100 # meters
nPixelsPerLineScan = 900

#  Count number of lines in LCF file (number of line scans)
with open(lcfFile) as infile:
	nLineScans = sum(1 for _ in infile)

deltaLat = (swathWidth/nPixelsPerLineScan)*np.cos(directionFOV*(math.pi/180.0))/earthRadius
deltaLong = (swathWidth/nPixelsPerLineScan)*np.sin(directionFOV*(math.pi/180.0))/earthRadius
'''

