import rasterio
import matplotlib.pyplot as plt

bil = rasterio.open("data\\manual-26\\20171206_21h20m_Pika_L_26.bil")

image = bil.read(240)
plt.imshow(image)
plt.show()

from spectral import *
import spectral.io.envi as envi

hdr = "data\\manual-26\\20171206_21h20m_Pika_L_26.bil.hdr"
bil = "data\\manual-26\\20171206_21h20m_Pika_L_26.bil"
img = envi.open(hdr, bil)

imshow(img)

view_cube(img)
