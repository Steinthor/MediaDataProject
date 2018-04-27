# -*- coding: utf-8 -*-
"""
    Title:          JPG test
    Authors:        Steinþór Jasonarson
    Date:           04.04.2018
    Description:    test code in regards to the JPG standard

"""

import cv2
import imageio
import glymur
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['image.cmap'] = 'gray'

image_name = "beach_wood"
image_ending = ".png"

load_path = "data/load/"
save_path = "data/save/"
img = imageio.imread(load_path+image_name+image_ending)

# plt.imshow(img, vmin=0, vmax=255)
# plt.show()

# Saving to JPEG 2000 through the imageio library

imageio.imwrite(save_path+image_name+"_01"+".jp2", img, "JP2-FI")
