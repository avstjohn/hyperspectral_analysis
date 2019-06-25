import spectral.io.envi as envi
from spectral import *
import numpy as np
import scipy.misc as sm
import matplotlib.cm as cm
from PIL import Image

#  Read command line arguments
hdrFile = sys.argv[1]
bilFile = sys.argv[2]
fileIndex = int(sys.argv[3])

#  Open ENVI-formatted header file and BIL binary
img = envi.open(hdrFile, bilFile)

#  Define band numbers for bands of interest
#nirBandNo = 166
#redBandNo = 115
#greenBandNo = 73
#blueBandNo = 30
nirBandNo = 83
redBandNo = 58
greenBandNo = 36
blueBandNo = 15


#  Grab the bands of color from the tensor
nir = img[:, :, nirBandNo]
red = img[:, :, redBandNo]
green = img[:, :, greenBandNo]
blue = img[:, :, blueBandNo]

#  Create RGB image
rgbFile = '04-05-2016/rgb%d.jpg' % fileIndex
save_rgb(rgbFile, img, [redBandNo, greenBandNo, blueBandNo])

#  Calculate NDVI 
ndvi = (nir - red) / (nir + red)
ndvi = np.squeeze(ndvi, axis = 2)

#  Use PIL to convert array to an image
ndviImage = Image.fromarray(cm.RdYlGn(ndvi, bytes = True))
ndviFile = '04-05-2016/ndvi%d.jpg' % fileIndex
sm.toimage(ndviImage, cmin= 0.0 , cmax = 1.0).save(ndviFile)

