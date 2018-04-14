# -*- coding: utf-8 -*-
"""
    Title:          BPG test
    Authors:        Philipp Brandauer
    Date:           14.04.2018
    Description:    Demo file to convert PNG to BPG file format

"""
from convert import Convert
import imageio
import subprocess

path_in = './data/CoMoFoD/'
path_out = './data/converted/'
path_jpegxr = './tools/nconvert/nconvert.exe'

img = imageio.imread(path_in + 'test_png.png', format='PNG-FI')
img_size = img.size

# Saving to BPG through command line tool libbpg
result = subprocess.run([path_jpegxr, '-out', 'jxr', '-q', '50', '-o', path_out + 'test.jxr', path_in + 'test_png.png'])
print(result)


c = Convert()
c.convert_jpegxr('test_gross.png', [10, 20, 30, 40, 50, 60, 70, 80, 90])