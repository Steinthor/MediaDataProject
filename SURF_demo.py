import imageio
import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance

#blabla
image_name = "002_F"
image_ending = ".png"

load_path = "data/CoMoFoD/"
img_test = imageio.imread(load_path+image_name+image_ending)

surf = cv2.xfeatures2d.SIFT_create()
(kps, descs) = surf.detectAndCompute(img_test, None)
img_surf = cv2.drawKeypoints(img_test, kps, None, color=(0, 255, 0), flags=0)

Tr = 0.5    #treshold ratio
Tc = 10     #threshold cluster

dlist = descs.tolist()
dist = np.zeros([descs.shape[0], 1])
distlist = dist.tolist()
kddlist = list(zip(kps,dlist,distlist)) # keypoint, descriptor, distance list

cluster = list()

p = 0


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

mindist = (0,0,0)

while mindist[0] < Tc:
    mindist = (Tc+1,0,0)
    for i in np.arange(len(cluster)):
        for j in np.arange(i):
            tempdist = distance.euclidean(cluster[i][0], cluster[j][0])
            if tempdist < mindist[0]:
                mindist = (tempdist,i,j)
    if mindist[0] < Tc:
        tempi = cluster.pop(mindist[1])
        tempj = cluster.pop(mindist[2])
        new_k = tempi[1] + tempj[1]
        new_x = (tempi[1] * tempi[0][0] + tempj[0][0] * tempj[1]) / new_k
        new_y = (tempi[1] * tempi[0][1] + tempj[0][1] * tempj[1]) / new_k
        cluster.append(([new_x,new_y], new_k, 0))

clustercount = 0
for i in np.arange(len(cluster)):
    if cluster[i][1] >= 4:
        clustercount = clustercount +1

if clustercount >= 2:
    print("copy move attack detected")
else:
    print("no copy move attack detected")












