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
