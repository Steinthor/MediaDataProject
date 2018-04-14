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

# Saving to JPEG 2000 through Glymur library

kargs_j2p = {"cratios": [50]}
j = glymur.Jp2k(save_path+image_name+"_02"+".jp2", img, **kargs_j2p)

# all possible arguments in kargs_j2p:
# shape : tuple, optional      ; Size of image data, only required when image_data is not provided.
# cbsize : tuple, optional     ; Code block size (NROWS, NCOLS)
# cinema2k : int, optional     ; Frames per second, either 24 or 48.
# cinema4k : bool, optional    ; Set to True to specify Cinema4K mode, defaults to false.
# colorspace : {'rgb', 'gray'} ; The image color space.
# cratios : iterable, optional ; Compression ratios for successive layers.
# eph : bool, optional         ; If true, write SOP marker after each header packet.
# grid_offset : tuple, optional; Offset (DY, DX) of the origin of the image in the reference grid.
# irreversible : bool, optional; If true, use the irreversible DWT 9-7 transform.
# mct : bool, optional         ; Usage of the multi component transform.  If not specified, defaults
#                                to True if the color space is RGB.
# modesw : int, optional       ; mode switch
#                1 = BYPASS(LAZY)
#                2 = RESET
#                4 = RESTART(TERMALL)
#                8 = VSC
#                16 = ERTERM(SEGTERM)
#                32 = SEGMARK(SEGSYM)
# numres : int, optional        ; Number of resolutions.
# prog : {"LRCP" "RLCP", "RPCL", "PCRL", "CPRL"} ; Progression order.
# psnr : iterable, optional     ; Different PSNR for successive layers.
# psizes : list, optional       ; List of precinct sizes, each precinct size tuple is defined in (height x width).
# sop : bool, optional          ; If true, write SOP marker before each packet.
# subsam : tuple, optional      ; Subsampling factors (dy, dx).
# tilesize : tuple, optional    ; Tile size in terms of (numrows, numcols), not (X, Y).
# verbose : bool, optional      ; Print informational messages produced by the OpenJPEG library.