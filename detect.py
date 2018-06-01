# -*- coding: utf-8 -*-
"""
    Title:          Multimedia Data Formats
    Date:           01.06.2018
    Description:    
"""
import cv2
import numpy as np
from scipy.spatial import distance

class Detect:

    def __init__(self):
        return None

    def detect_all(self, keypoint_descriptors):
        """detect_all(in_file):
        Detects a copy-move attack in a given file with these methods:
        - SIFT (concentrate on those two for now)
        - SURF
        """
        results = {'ORB': self.detect(keypoint_descriptors['ORB']),
                   'BRISK': self.detect(keypoint_descriptors['BRISK']),
                   'SIFT': self.detect(keypoint_descriptors['SIFT']),
                   'SURF': self.detect(keypoint_descriptors['SURF'])}
        return results


    def detect(self, keypoint_descriptors, Tr=0.5, Tc=10,norm= cv2.NORM_L2):
        """ detectSURF(img_file)
        detects a copy-move attack within a given filename
        """
        kps = keypoint_descriptors['keypoints']
        descs = keypoint_descriptors['descriptors']

        # instantiation of the BruteForceMatcher class
        bf = cv2.BFMatcher(norm)
        # the knnMatch returns for each descriptor out of the queryDescriptors the k nearest (with respect to the used norm)
        # descriptors out of the trainDescriptors
        kmatch = bf.knnMatch(queryDescriptors=descs, trainDescriptors=descs, k=3)
        # create the clusterlist, one entry represents one cluster and should contain the mean x and y coordinate
        # of the cluster members, the number keypoints in this cluster and a placeholder for the later distance calculation.
        cluster = list()
        # ratio test, if the ratio of the distance from the nearest over the second nearest descriptor is less than the threshold Tr
        # cluster the query keypoint with the nearest train keypoint.
        for i in np.arange(len(kmatch)):
            if kmatch[i][0] != 0:
                if (kmatch[i][1].distance / kmatch[i][2].distance) < Tr:
                    # for the agglomerative hierarchical clustering we compare the distances between the centroid
                    # (the mean x and y coordinate of all keypoints of the cluster) from two cluster.
                    # therefore add the mean x and y coordinates and the number of cluster members to the cluster list
                    x = (kps[kmatch[i][1].queryIdx].pt[0] + kps[kmatch[i][1].trainIdx].pt[0]) / 2
                    y = (kps[kmatch[i][1].queryIdx].pt[1] + kps[kmatch[i][1].trainIdx].pt[1]) / 2
                    cluster.append(([x, y], 2, 0))
                    # to avoid duplicate cluster set the match result for the already added descriptor to zero
                    kmatch[kmatch[i][1].trainIdx] = (0, 0, 0)

        # agglomerative hierarchical clustering, merge the two nearest (distance between the centroids) if the distacne
        # is less than the threshold Tc
        # to store the actual minimum distance and the index of the according two cluster
        mindist = (0, 0, 0)
        # store the number of cluster with more than 3 Keypoints
        clustercount = 0
        # do the clustering until the minimum distance is greater than the threshold or more than 2 cluster has more than 3 Keypoints
        while mindist[0] < Tc and clustercount < 2:
            mindist = (Tc + 1, 0, 0)
            for i in np.arange(len(cluster)):
                for j in np.arange(i):
                    tempdist = distance.euclidean(cluster[i][0], cluster[j][0])
                    if tempdist < mindist[0]:
                          mindist = (tempdist, i, j)

            if mindist[0] < Tc:
                tempi = cluster.pop(mindist[1])
                tempj = cluster.pop(mindist[2])
                new_k = tempi[1] + tempj[1]
                new_x = (tempi[1] * tempi[0][0] + tempj[0][0] * tempj[1]) / new_k
                new_y = (tempi[1] * tempi[0][1] + tempj[0][1] * tempj[1]) / new_k
                cluster.append(([new_x, new_y], new_k, 0))
                # to avoid to increase the clustercount for cluster which already had more than 3 Keypoints
                if tempi[1] <= 3 and tempj[1] <= 3:
                    clustercount = clustercount + 1

        if clustercount >= 2:
            # Copy move attack detected
            return True
        else:
            # No detection
            return False



