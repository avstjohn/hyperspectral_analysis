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
	#  ceiling function yields integer ~ discrete pixels
	pixelShift.append(int(m.ceil(diff_lon_meters[i]/ pixelWidth_meter[i])))

maxShift = max(pixelShift)
minShift = min(pixelShift)
