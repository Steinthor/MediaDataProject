from os import path, listdir
from time import time
from datetime import datetime
import re
import json
from keypoint import Keypoint
from detect import Detect


def save_obj(dictionary, name):
    with open(name + '.json', 'w') as f:
        json.dump(dictionary, f, indent=4)

def load_obj(name):
    with open(name + '.json', 'rb') as f:
        return json.load(f)
    
def dump(dictionary):
    print(json.dumps(dictionary, indent=4))


# Path to dataset

path_infiles='./data/CoMoFoD_small/'

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
    
    print(file)
    print('current time, after keypoint detection: ' + str(elapsed_time))

    result[fname][extension][ratio] = DET.detect_all(keypoints)

    elapsed_time = time() - current_time
    print('Current time, after copy/move attack detection: ' + str(elapsed_time))

elapsed_time = time() - current_time
print('Elapsed time in seconds: ' + str(elapsed_time))

# Save data result data to file
save_obj(result, 'result_{date:%Y_%m_%d__%H_%M_%S}'.format( date=datetime.now()))
dump(result)
