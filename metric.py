# As the metric is not well understood, here is analysis of the metric itself.
# 4 categories:
# 1) True positive 'Tp', a fake image is detected as fake
# 2) False negative 'Fn', a fake image is _not_ detected as fake
# 3) False positive ' Fp', an original image is detected as fake
# 4) True negative 'Tn', an original image is _not_ detected as fake
# p = Tp / (Tp + Fp)
# r = Tp / (Tp + Fn)
# F1 = 2 * p*r / (p+r)
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

N = 100         # number of images we hypothetically start with
F1 = np.zeros((N, N))
Tp = N/2        # half of the images have a copy-move attack in them.
Fn = 0
Fp = 0
Tn = N/2        # half of the images do not have a copy-move attack in them.
z = 0
for i in np.arange(N):
    for j in np.arange(i+1):
        t_Fn = j
        t_Fp = i - j
        t_Tp = Tp - t_Fn
        t_Tn = Tn - t_Fp
        if np.abs(t_Tp) + np.abs(t_Fn) > 50:
            continue
        if np.abs(t_Tn) + np.abs(t_Fp) > 50:
            continue
        if max([t_Tp, t_Fp]) > 0:
            p = t_Tp / (t_Tp + t_Fp)
        if max([t_Tp, t_Fn]) > 0:
            r = t_Tp / (t_Tp + t_Fn)
        if max(p, r) > 0:
            F1[i][j] = 2 * p*r / (p+r)

x, y = F1.nonzero()
z = F1[x, y]


fig = plt.figure()
fig.suptitle("F1 values with varying number of Fp or Fn")

x1, y1 = ((F1 < 0.6666)*(F1 > 0)).nonzero()
z1 = F1[x1, y1]
x2, y2 = ((F1 < 1)*(F1 > 0.6666)).nonzero()
z2 = F1[x2, y2]

ax2 = fig.add_subplot(111, projection='3d')
ax2.scatter(x1, y1, z1, c='r')
ax2.scatter(x2, y2, z2, c='g')
ax2.set_xlabel('Tn decreasing')
ax2.set_ylabel('Tp decreasing')
ax2.set_zlabel('F1 value')


plt.show()
