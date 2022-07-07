
import h5py
import numpy as np
from PIL import Image

hdf = h5py.File("0.hdf5",'r')
#array = hdf["Photos/Image 1"][:]
array = hdf["colors"][:]
img = Image.fromarray(array.astype('uint8'), 'RGB')
img.save("yourimage.jpg", "JPEG")
img.save("yourimage.png", "PNG")
img.show()



