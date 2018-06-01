import numpy as np
import cv2
import imageio
from matplotlib import pyplot as plt

image_name = "001_F"
image_ending = ".png"

load_path = "data/CoMoFoD/"
img = imageio.imread(load_path+image_name+image_ending, format="PNG-FI")

# Initiate FAST detector
fast = cv2.FastFeatureDetector_create()
# Cause FAST is just a detector for keypoints
# Additionally BRISK is used to get descriptors
br = cv2.BRISK_create()

# find the keypoints with FAST
kp = fast.detect(img, None)

# compute the descriptors with BRISK
kp, des = br.compute(img,  kp)

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
