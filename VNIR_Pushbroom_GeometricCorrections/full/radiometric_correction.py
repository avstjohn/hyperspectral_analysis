# Aerial Analytics: hyperspectral data corrections and cleaning
# Alex St. John, April 12th, 2016
#
# Need: Hyperspectral sensor needs radiometric corrections to the reflectance values ot remove spectral 
#	contamination due to the sun, atmosphere, and instrument response. 
#
# Usage: python radiometric_correction.py <path to CSV file>
#
from __future__ import division
from __future__ import print_function

import spectral.io.envi as envi
from spectral import *
import numpy as np
import scipy.misc as sm
import matplotlib.cm as cm
from PIL import Image
import math
from itertools import izip
import csv

with open('spectralInfo.csv', 'w') as infile:
	reader = csv.reader(infile, delimiter = ',')
