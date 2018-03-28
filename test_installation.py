# -*- coding: utf-8 -*-
#
#   Title:          Multimedia Data Formats
#   Authors:        Philipp Brandauer
#   Date:           27.03.2018
#   Description:    Test all components needed for the project.
#

import cv2
import imageio
import matplotlib.pyplot as plt

# Check library versions 
print(cv2.__version__)          # should be 3.4.1
print(imageio.__version__)      # should be 2.3.0


# Check image reading
img_png = imageio.imread("data/test/test_png.png", format="PNG-FI")
img_jpeg = imageio.imread("data/test/test_jpeg.jpg", format="JPEG-FI")
img_jp2 = imageio.imread("data/test/test_jpeg2000.jp2", format="JP2-FI")
img_jxr = imageio.imread("data/test/test_jpegxr.jxr", format="JPEG-XR-FI")

fig, axes = plt.subplots(1, 4)
axes[0].imshow(img_png)
axes[0].set_title('PNG')
axes[0].axis('off')
axes[1].imshow(img_jpeg)
axes[1].set_title('JPEG')
axes[1].axis('off')
axes[2].imshow(img_jp2)
axes[2].set_title('JPEG2000')
axes[2].axis('off')
axes[3].imshow(img_jxr)
axes[3].set_title('JPEG XR')
axes[3].axis('off')
plt.show()

# Check image writing
#PNG:       https://imageio.readthedocs.io/en/latest/format_png-fi.html#png-fi
#JPEG:      https://imageio.readthedocs.io/en/latest/format_jpeg-fi.html
#JPEG2000:  https://imageio.readthedocs.io/en/latest/format_jp2-fi.html#jp2-fi
#JPEG-XR:   https://imageio.readthedocs.io/en/stable/format_jpeg-xr-fi.html#jpeg-xr-fi
kargs_png = {"compression": 9, "quantize": 200}
kargs_jpeg = {"quality": 10}
kargs_jp2 = {"FREE_IMAGE_SAVE_FLAGS":10}
imageio.imwrite("data/test/out_test_png.png", img_png, "PNG-FI", **kargs_png)
imageio.imwrite("data/test/out_test_jpeg.jpg", img_png, "JPEG-FI", **kargs_jpeg)
imageio.imwrite("data/test/out_test_jpeg2000.jp2", img_png, "JP2-FI")
imageio.imwrite("data/test/out_test_jpegxr.jxr", img_png, "JPEG-XR-FI")





