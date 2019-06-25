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
