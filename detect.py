import imageio
from os import path, listdir
from time import time
import glymur
import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance
from keypoint import Keypoint

class Detect:

    def __init__(self):
        return None

    def doit(self):
        """doit():
        Detects a copy-move attack with all images in a given path
        """
        in_list = listdir(self.path)
        current_time = time()
        for file in in_list:
            filename, extension = path.splitext(path.basename(file))
            self.detect_all(filename, extension)
        elapsed_time = time() - current_time
        print('Elapsed time in seconds: ' + str(elapsed_time))

    def detect_all(self, keypoints):
        """detect_all(in_file):
        Detects a copy-move attack in a given file with these methods:
        - SURF
        """
        return self.detectSURF(keypoints['SURF'])

    def detectSURF(self, surf):
        """ detectSURF(img_file)
        detects a copy-move attack within a given filename
        """
        # img = self.loadImg(filename)
        # print(self.path + filename + extension)
        # img = self.load_img(filename, extension)

        #surf = cv2.xfeatures2d.SIFT_create()
        #(kps, descs) = surf.detectAndCompute(img, None)
        #img_surf = cv2.drawKeypoints(img, kps, None, color=(0, 255, 0), flags=0)
        current_time = time()
        kps = surf['keypoints']
        descs = surf['descriptors']

        Tr = 0.5    #treshold ratio
        Tc = 10     #threshold cluster
        
        dlist = descs.tolist()
        dist = np.zeros([descs.shape[0], 1])
        distlist = dist.tolist()
        kddlist = list(zip(kps,dlist,distlist)) # keypoint, descriptor, distance list
        
        cluster = list()

        while len(kddlist) != 0:
            tempcomp = kddlist.pop()
            for i in np.arange(len(kddlist)):
                kddlist[i] = (kddlist[i][0],kddlist[i][1], distance.euclidean(tempcomp[1], kddlist[i][1]))
            kddlist.sort(key=lambda tup: tup[2])
            k = 0
            ratio = 0
            while ratio < Tr:
                if k+2 >= len(kddlist):
                    break
                ratio = kddlist[k][2]/kddlist[k+1][2]
                k = k+1
            if k > 1:
                x = tempcomp[0].pt[0]
                y = tempcomp[0].pt[1]
                for j in np.arange(k-1):
                    x = x + kddlist[0][0].pt[0]
                    y = y + kddlist[0][0].pt[1]
                    kddlist.pop(0)
                cluster.append(([x/k,y/k],k,0))

        elapsed_time = time() - current_time
        print('Elapsed time after finding distances: ' + str(elapsed_time))

        found = True

        while found:
            found = False
            for i in np.arange(len(cluster)):
                for j in np.arange(i):
                    tempdist = distance.euclidean(cluster[i][0], cluster[j][0])
                    if tempdist < Tc:
                        tempi = cluster.pop(i)
                        tempj = cluster.pop(j)
                        new_k = tempi[1] + tempj[1]
                        new_x = (tempi[1] * tempi[0][0] + tempj[0][0] * tempj[1]) / new_k
                        new_y = (tempi[1] * tempi[0][1] + tempj[0][1] * tempj[1]) / new_k
                        cluster.append(([new_x,new_y], new_k, 0))
                        found = True
                        break
                if found:
                    break
                
        
        clustercount = 0
        for i in np.arange(len(cluster)):
            if cluster[i][1] >= 4:
                clustercount = clustercount +1
        
        if clustercount >= 2:
            print("copy move attack detected")
        else:
            print("no copy move attack detected")

        elapsed_time = time() - current_time
        print('Elapsed time after clustering: ' + str(elapsed_time))

        

        # plt.imshow(img)
        # plt.show()

    def load_img(self, filename, extension):
        # need code to fix loading bpgs, import libbpg in some way..
        if extension == ".jp2":
            jp2 = glymur.Jp2k(self.path + filename + extension)
            img = jp2[:]
        else:
            img = imageio.imread(self.path + filename + extension)
        return img
