# -*- coding: utf-8 -*-
"""
    Title:          JPG test
    Authors:        Steinþór Jasonarson
    Date:           04.04.2018
    Description:    test code in regards to the JPG standard

"""

import os
import imageio
import subprocess
import matplotlib.pyplot as plt

plt.rcParams['image.cmap'] = 'gray'

image_name = "beach_wood"
image_ending = ".png"

load_path = "data/load/"
save_path = "data/save/"
img = imageio.imread(load_path+image_name+image_ending)

# plt.imshow(img, vmin=0, vmax=255)
# plt.show()

# Saving to JPEG 2000 through command line tool

imageio.imwrite(save_path+image_name+"_03"+".bmp", img, "BMP")
result = subprocess.call(['opj_compress.exe', '-i', '../../'+save_path+image_name+"_03.bmp", '-r', '50', '-o', '../../'+save_path+image_name+'_03.jp2'], cwd='tools/openjpeg')