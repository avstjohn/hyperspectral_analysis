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

