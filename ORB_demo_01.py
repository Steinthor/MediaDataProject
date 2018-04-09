import numpy as np
import cv2
import imageio
from matplotlib import pyplot as plt

image_name = "beach_wood"
image_ending = ".png"

load_path = "data/load/"
img = imageio.imread(load_path+image_name+image_ending)

# Initiate STAR detector
orb = cv2.ORB_create()

# find the keypoints with ORB
kp = orb.detect(img, None)

# compute the descriptors with ORB
kp, des = orb.compute(img, kp)

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
