import numpy as np
import cv2
import imageio
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans


def orb_detect(des):

    temp_array = np.zeros((des.shape[0], des.shape[0], 1), dtype=np.float64)
    # temp_array = np.zeros((4, 4, 1), dtype=np.float64)
    for base in range(des.shape[0]):
        # the base descriptor is compared to the others
        for other in range(base+1, des.shape[0]):
            for i in range(des.shape[1]):
                #  number in the 'other' descriptor vector gets compared to base
                temp_array[base, other] = temp_array[base, other] + (float(des[base, i]) - float(des[other, i]))**2
            temp_array[base, other] = np.sqrt(temp_array[base, other])
    temp_array = np.reshape(temp_array, (-1, 1))
    temp_array.sort(axis=0)
    temp_array = np.trim_zeros(temp_array)
    print(temp_array)
    diff_array = np.diff(temp_array, axis=0)
    diff_array.sort(axis=0)
    print(diff_array)

    # Number of clusters
    kmeans = KMeans(n_clusters=3)
    # Fitting the input data
    kmeans = kmeans.fit(diff_array)
    # Getting the cluster labels
    labels = kmeans.predict(diff_array)
    # Centroid values
    centroids = kmeans.cluster_centers_
    centroids.sort(axis=0)
    print("centroids: ")
    print(centroids)  # From sci-kit learn
    print(labels)


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