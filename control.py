import imageio
from os import path, listdir
from time import time
import glymur
import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance
from keypoint import Keypoint
from detect import Detect
import pickle
import re
import sys

# Reference:
# https://stackoverflow.com/questions/15785719/how-to-print-a-dictionary-line-by-line-in-python
def dump(obj, nested_level=0, output=sys.stdout):
    spacing = '   '
    if type(obj) == dict:
        print('%s{' % ((nested_level) * spacing))
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print('%s%s:' % ((nested_level + 1) * spacing, k))
                dump(v, nested_level + 1, output)
            else:
                print('%s%s: %s' % ((nested_level + 1) * spacing, k, v))
        print('%s}' % (nested_level * spacing))
    elif type(obj) == list:
        print('%s[' % ((nested_level) * spacing))
        for v in obj:
            if hasattr(v, '__iter__'):
                dump(v, nested_level + 1, output)
            else:
                print('%s%s' % ((nested_level + 1) * spacing, v))
        print('%s]' % ((nested_level) * spacing))
    else:
        print('%s%s' % (nested_level * spacing, obj))

# Reference:
# https://stackoverflow.com/questions/19201290/how-to-save-a-dictionary-to-a-file
def save_obj(obj, name):
    with open(name + '.dic', 'wb') as f:
        pickle.dump(obj, f, protocol=0)


def load_obj(name):
    with open(name + '.dic', 'rb') as f:
        return pickle.load(f)

path_infiles='./data/converted/'

in_list = listdir(path_infiles)
current_time = time()
KP = Keypoint()
DET = Detect()
result = {}

for file in in_list:
    filename, extension = path.splitext(path.basename(file))

    # create a new dictionary for each filename, add keys:
    #   'path', value: the path to the file
    #   'filename', value: the filename without the extension
    #   'extension', value: the ending of the file

    fname = re.search('^\d+_[FO]', filename).group(0)  # technically the original file name without classifiers

    if fname not in result:
        result[fname] = {}

    if extension not in result[fname]:
        result[fname][extension] = {}

    # check from filename if file is an Original or Fake, add to dictionary as key:
    #   'Fake', value: true/false

    m = re.search(r'(_F)', filename)
    if m:
        result[fname]['Fake'] = True
    else:
        result[fname]['Fake'] = False

    # check from filename the compression of the file and add truth result into a dictionary;
    #   '10' (the ratio), values: true/false whether it found the copy/move attack in that compression or not

    m = re.search(r'(?<=_)\d+', filename)
    if m:
        ratio = m.group(0)
    else:
        ratio = '0'

    if ratio not in result[fname][extension]:
        result[fname][extension][ratio] = {}

    keypoints = KP.compute_all(path_infiles+filename+extension)

    elapsed_time = time() - current_time
    print('current time, after keypoint detection: ' + str(elapsed_time))

    result[fname][extension][ratio] = DET.detect_all(keypoints)

    elapsed_time = time() - current_time
    print('Current time, after copy/move attack detection: ' + str(elapsed_time))

elapsed_time = time() - current_time
print('Elapsed time in seconds: ' + str(elapsed_time))
# dump(result)

# save the dictionary as a file
save_obj(result, 'result00')

# load a dictionary from a file
test = load_obj('result00')
dump(test)


# use the data for analysis.
# probably better to use another python script for the analysis.
