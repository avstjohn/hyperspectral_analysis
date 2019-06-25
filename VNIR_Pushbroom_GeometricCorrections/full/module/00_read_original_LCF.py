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
