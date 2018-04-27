import imageio
import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance

#blabla
image_name = "001_F"
image_ending = ".png"

load_path = "data/CoMoFoD/"
img_test = imageio.imread(load_path+image_name+image_ending, format="PNG-FI")

surf = cv2.xfeatures2d.SIFT_create()
(kps, descs) = surf.detectAndCompute(img_test, None)
img_surf = cv2.drawKeypoints(img_test, kps, None, color=(0, 255, 0), flags=0)

dist = np.empty([descs.shape[0],2])
print(descs.shape)
for i in np.arange(descs.shape[0]):
    for j in np.arange(descs.shape[0]):
        dist[j][0] = distance.euclidean(descs[i],descs[j])
        dist[j][1] = j

    dist = dist[np.argsort(dist[:, 0])]
    print(dist)

    k = 0
    q = 0
    while q < 0.6:
        k = k + 1
        q = dist[k]/dist[k+1]



#dst = distance.euclidean(a,b)

fig, axes = plt.subplots(1, 2)
axes[0].imshow(img_test)
axes[0].set_title('original image')
axes[0].axis('off')
axes[1].imshow(img_surf)
axes[1].set_title('with keypoints')
axes[1].axis('off')
plt.show()
