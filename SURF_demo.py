import imageio
import cv2
import matplotlib.pyplot as plt

image_name = "001_F"
image_ending = ".png"

load_path = "data/CoMoFoD/"
img_test = imageio.imread(load_path+image_name+image_ending, format="PNG-FI")

surf = cv2.xfeatures2d.SURF_create()
(kps, descs) = surf.detectAndCompute(img_test, None)
img_surf = cv2.drawKeypoints(img_test, kps, None, color=(0, 255, 0), flags=0)



fig, axes = plt.subplots(1, 2)
axes[0].imshow(img_test)
axes[0].set_title('original image')
axes[0].axis('off')
axes[1].imshow(img_surf)
axes[1].set_title('with keypoints')
axes[1].axis('off')
plt.show()
