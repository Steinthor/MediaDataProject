# -*- coding: utf-8 -*-
"""
    Title:          JPG test
    Authors:        Steinþór Jasonarson
    Date:           04.04.2018
    Description:    test code in regards to the JPG standard

"""

import cv2
import imageio
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['image.cmap'] = 'gray'

image_name = "beach_wood"
image_ending = ".png"

load_path = "data/load/"
save_path = "data/save/"
img = imageio.imread(load_path+image_name+image_ending)

plt.imshow(img, vmin=0, vmax=255)
plt.show()

# Saving to JPG

# The compression factor of the saved image (1..100), higher numbers result in higher quality but larger file size.
# Default 75.
# from pillow:  Values above 95 should be avoided; 100 disables portions of the JPEG compression algorithm, and results
# in large files with hardly any gain in image quality.
quality = 75

# Save as a progressive JPEG file (e.g. for images on the web). Default False.
progressive = True

# On saving, compute optimal Huffman coding tables (can reduce a few percent of file size). Default False.
optimize = True

# The pixel density, (x,y).
dpi = (10, 10)

# If present and true, the image is stored with the provided ICC profile. If this parameter is not provided, the image
#  will be saved with no profile attached.
# from pillow:  To preserve the existing profile:
# im.save(filename, 'jpeg', icc_profile=im.info.get('icc_profile'))
# icc_profile =

# If present, the image will be stored with the provided raw EXIF data.
# exif = dict

# Sets the subsampling for the encoder. See Pillow docs for details.
#   keep: Only valid for JPEG files, will retain the original image setting.
#   4:4:4, 4:2:2, 4:1:1: Specific sampling values
#   -1: equivalent to keep
#   0: equivalent to 4:4:4
#   1: equivalent to 4:2:2
#   2: equivalent to 4:1:1
subsampling = 0

# Set the qtables for the encoder. See Pillow docs for details.
#  Use with caution. qtables can be one of several types of values:
#     a string, naming a preset, e.g. keep, web_low, or web_high
#     a list, tuple, or dictionary (with integer keys = range(len(keys))) of lists of 64 integers. There must be between 2 and 4 tables.
#qtables =

kargs_jpeg = {"quality": quality, "progressive": progressive, "optimize": optimize, "dpi": dpi, "subsampling": subsampling}
imageio.imwrite(save_path+image_name+"_"+str(quality)+".jpg", img, "JPEG-PIL", **kargs_jpeg)