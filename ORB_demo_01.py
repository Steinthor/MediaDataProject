import numpy as np
import cv2
import imageio
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

def orb_detect (des):

    for base in range(0): #des.shape[0]):
        # the base descriptor is compared to the others
        for other in range(des.shape[0]):
            if base == other:
                continue
            else
                temp = zeros(des.shape[1])
                for i in range(des.shape[1]):
                    #each number in the 'other' descriptor vector gets compared to base
                    temp[i] = 



    temp = np.diff(des)
    temp = np.linalg.norm(temp, axis=1)

    temp.sort()

    temp2 = np.diff(temp)
    temp2.sort()

    temp2 = np.reshape(temp2, (-1,1))
    print( temp2.shape )
    # Number of clusters
    kmeans = KMeans(n_clusters=3)
    # Fitting the input data
    kmeans = kmeans.fit(temp2)
    # Getting the cluster labels
    labels = kmeans.predict(temp2)
    # Centroid values
    centroids = kmeans.cluster_centers_
    print(centroids[0])  # From sci-kit learn
    #print(labels)


image_name = "001_F"
image_ending = ".png"

load_path = "data/CoMoFoD/"
img = imageio.imread(load_path+image_name+image_ending, format="PNG-FI")

# Initiate STAR detector
orb = cv2.ORB_create()

# find the keypoints with ORB
kp = orb.detect(img, None)

# compute the descriptors with ORB
kp, des = orb.compute(img, kp)

orb_detect(des)

"""
# draw only keypoints location,not size and orientation
img2 = np.copy(img)
cv2.drawKeypoints(img, kp, img2, color=(0, 255, 0), flags=4)

fig, axes = plt.subplots(1, 2)
axes[0].imshow(img)
axes[0].set_title('original')
axes[0].axis('off')
axes[1].imshow(img2)
axes[1].set_title('with keypoints')
axes[1].axis('off')
plt.show()
"""