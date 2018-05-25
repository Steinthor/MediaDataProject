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
        self.detectSURF(keypoints['SURF'])

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
        kps = surf['keypoints']
        descs = surf['descriptors']

        dist = np.empty([descs.shape[0], 2])
        cluster = np.zeros([descs.shape[0], 4])
        print(descs.shape)
        p = 0
        c = 0

        for i in np.arange(descs.shape[0]):
            if descs[i][0] != -1:
                for j in np.arange(descs.shape[0]):
                    dist[j][0] = distance.euclidean(descs[i], descs[j])
                    dist[j][1] = j
                dist = dist[np.argsort(dist[:, 0])]
                # print(dist)
                # print('vergleich')
                k = 0
                q = 0
                T = 0.5
                while q < T:
                    k = k + 1
                    q = dist[k][0] / dist[k + 1][0]
                    # print(q)
                    # print('--------')
                if k >= 2:
                    descs[i][0] = -1
                    cluster[p][0] = c
                    cluster[p][1] = int(dist[0][1])
                    cluster[p][2] = np.mean(kps[int(dist[0][1])].pt[0])
                    cluster[p][3] = np.mean(kps[int(dist[0][1])].pt[1])
                    p = p + 1
                    for l in np.arange(k - 1):
                        descs[int(dist[l + 1][1])][0] = -1
                        cluster[p][0] = c
                        cluster[p][1] = int(dist[l + 1][1])
                        cluster[p][2] = np.mean(kps[int(dist[l + 1][1])].pt[0])
                        cluster[p][3] = np.mean(kps[int(dist[l + 1][1])].pt[1])
                        p = p + 1
                        # print(k)
                        # print( i,"equal to",dist[l+1][1])
                    c = c + 1

        cluster = cluster[~np.all(cluster == 0, axis=1)]
        endc = c
        distT = 10
        distTT = 0
        while distTT < distT:
            clustercomp = np.zeros([c, 2])
            for i in np.arange(c):
                sum_x = 0
                sum_y = 0
                n = 0
                for j in np.arange(cluster.shape[0]):
                    if cluster[j][0] == i:
                        sum_x = sum_x + cluster[j][2]
                        sum_y = sum_y + cluster[j][3]
                        n = n + 1
                if n != 0:
                    clustercomp[i][0] = sum_x / n
                    clustercomp[i][1] = sum_y / n
                else:
                    clustercomp[i][0] = 99999
                    clustercomp[i][1] = 99999
            clustdist = np.zeros([c, 3])
            for i in np.arange(c):
                tempdist01 = 99999
                tempj = 0
                tempi = 0
                for j in np.arange(c):
                    if i != j:
                        tempdist02 = distance.euclidean(clustercomp[i], clustercomp[j])
                        if tempdist02 < tempdist01:
                            tempdist01 = tempdist02
                            tempj = j
                            tempi = i
                clustdist[i][0] = tempdist01
                clustdist[i][1] = tempi
                clustdist[i][2] = tempj
            clustdist = clustdist[np.argsort(clustdist[:, 0])]
            distTT = clustdist[0][0]
            # print(distTT)
            # print(clustdist)
            if distTT < distT:
                for t in np.arange(cluster.shape[0]):
                    if cluster[t][0] == clustdist[0][2]:
                        cluster[t][0] = clustdist[0][1]
                        # print(cluster[t][0])
                        # print(clustdist[0][1])
                c = c - 1

        countclust = 0;
        for i in np.arange(endc):
            countelements = 0;
            for j in np.arange(cluster.shape[0]):
                if cluster[j][0] == i:
                    countelements = countelements + 1
            if countelements >= 4:
                countclust = countclust + 1

        if countclust > 2:
            print("copy move attack detected")
            return True
        else:
            print("no copy move attack detected")
            return False

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
