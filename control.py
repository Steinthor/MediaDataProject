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


def save_obj(obj, name ):
    with open(name + '.dic', 'w+') as f:
        pickle.dump(obj, f)


def load_obj(name ):
    with open(name + '.dic', 'r') as f:
        return pickle.load(f)

path_infiles='./data/converted/'

in_list = listdir(path_infiles)
current_time = time()
KP = Keypoint()
DET = Detect()
Result = {}

for file in in_list:
    filename, extension = path.splitext(path.basename(file))

    # create a new dictionary for each filename, add keys:
    #   'path', value: the path to the file
    #   'filename', value: the filename without the extension
    #   'extension', value: the ending of the file
    # check from filename if file is an Original or Fake, add to dictionary as key:
    #   'Fake', value: true/false
    # check from filename the compression of the file and add truth result into a dictionary;
    #   '10' (the ratio), values: true/false whether it found the copy/move attack in that compression or not
    # -> add all dictionaries into a single dictionary.
    # -> save the dictionary as a file
    # use the data in each dictionary for analysis.

    #keypoints = KP.compute_all(path_infiles+filename+extension)

    #elapsed_time = time() - current_time
    #print('current time, after keypoint detection: ' + str(elapsed_time))

    #test = DET.detect_all(keypoints)

    #elapsed_time = time() - current_time
    #print('Current time, after copy/move attack detection: ' + str(elapsed_time))


elapsed_time = time() - current_time
print('Elapsed time in seconds: ' + str(elapsed_time))

