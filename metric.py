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
fig2 = plt.figure()
fig2.suptitle("F1 values with varying number of Fp or Fn")
ax = fig.add_subplot(221, projection='3d')
ax.scatter(x, y, z, c='red', depthshade=True)
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Proportional value')
ax.set_title("Fake negatives sliding scale")

x1, y1 = ((F1 < 0.6666)*(F1 > 0)).nonzero()
z1 = F1[x1, y1]
x2, y2 = ((F1 < 1)*(F1 > 0.6666)).nonzero()
z2 = F1[x2, y2]

ax = fig.add_subplot(222, projection='3d')
ax2 = fig2.add_subplot(111, projection='3d')
ax.scatter(x1, y1, z1, c='r')
ax.scatter(x2, y2, z2, c='g')
ax.set_xlabel('Tn decreasing')
ax.set_ylabel('Tp decreasing')
ax.set_zlabel('F1 value')
ax.set_title("Tp and Tn decreasing")
ax2.scatter(x1, y1, z1, c='r')
ax2.scatter(x2, y2, z2, c='g')
ax2.set_xlabel('Tn decreasing')
ax2.set_ylabel('Tp decreasing')
ax2.set_zlabel('F1 value')

p = np.zeros(N)
r = np.zeros(N)
F1 = np.zeros(N)
Tp = N/2        # half of the images have a copy-move attack in them.
Fn = 0
Fp = 0
Tn = N/2        # half of the images do not have a copy-move attack in them.

for i in np.arange(N):
    if max(Tp, Fp) > 0:
        p[i] = Tp / (Tp + Fp)
    else:
        p[i] = 1
    if max(Tp, Fn) > 0:
        r[i] = Tp / (Tp + Fn)
    else:
        r[i] = 1
    if max(p[i], r[i]) > 0:
        F1[i] = 2 * p[i]*r[i] / (p[i]+r[i])
    if Tn > 0:
        Tn = Tn - 1
        Fp = Fp + 1
    elif Tp > 0:
        Tp = Tp - 1
        Fn = Fn + 1

x = np.arange(N)
ax = fig.add_subplot(224)
ax.plot(x, F1)
ax.set_title('First Tn decreasing, then Tp decreasing')

plt.show()
