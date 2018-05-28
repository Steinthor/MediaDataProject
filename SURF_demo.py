import imageio
import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance

#blabla
image_name = "test"
image_ending = ".JPG"

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


p = 0


bf = cv2.BFMatcher()
kmatch = bf.knnMatch(descs,trainDescriptors =descs,k=3)

cluster = list()

for i in np.arange(len(kmatch)):
    if kmatch[i][0] !=0:
        if (kmatch[i][1].distance/kmatch[i][2].distance) < Tr:
            x = (kps[kmatch[i][1].queryIdx].pt[0] + kps[kmatch[i][1].trainIdx].pt[0])/2
            y = (kps[kmatch[i][1].queryIdx].pt[1] + kps[kmatch[i][1].trainIdx].pt[1]) / 2
            cluster.append(([x , y ], 2, 0))
            kmatch[kmatch[i][1].trainIdx]= (0,0,0)



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












