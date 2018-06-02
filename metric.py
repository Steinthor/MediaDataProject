# As the metric is not well understood, here is analysis of the metric itself.
# 4 categories:
# 1) True positive 'Tp', a fake image is detected as fake
# 2) False negative 'Fn', a fake image is _not_ detected as fake
# 3) False positive ' Fp', an original image is detected as fake
# 4) True negative 'Tn', an original image is _not_ detected as fake
# p = Tp / (Tp + Fp)
# r = Tp / (Tp + Fn)
# F1 = 2 * p*r / (p+r)

import numpy as np
import matplotlib.pyplot as plt
N = 100         # number of images we hypothetically start with
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
    if max(Tp, Fn) > 0:
        r[i] = Tp / (Tp + Fn)
    if max(p[i], r[i]) > 0:
        F1[i] = 2 * p[i]*r[i] / (p[i]+r[i])
    if Tp > 0:
        Tp = Tp - 1
        Fn = Fn + 1

x = np.arange(N)
fig = plt.figure()

plt.subplot(2, 2, 1)
plt.plot(x, F1)
plt.ylabel("F1 value")
plt.title("Fake negatives sliding scale")

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
    if max(Tp, Fn) > 0:
        r[i] = Tp / (Tp + Fn)
    if max(p[i], r[i]) > 0:
        F1[i] = 2 * p[i]*r[i] / (p[i]+r[i])
    if Tn > 0:
        Tn = Tn - 1
        Fp = Fp + 1

x = np.arange(N)
plt.subplot(2, 2, 2)
plt.plot(x, F1)
plt.ylim(0, 1)
plt.title("Fake positives sliding scale")

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
    if max(Tp, Fn) > 0:
        r[i] = Tp / (Tp + Fn)
    if max(p[i], r[i]) > 0:
        F1[i] = 2 * p[i]*r[i] / (p[i]+r[i])
    if Tp >= Tn:
        Tp = Tp - 1
        Fn = Fn + 1
    else:
        Tn = Tn - 1
        Fp = Fp + 1

x = np.arange(N)
plt.subplot(2, 2, 3)
plt.plot(x, F1)
plt.ylim(0, 1)
plt.title("equal removal of Tp and Tn")

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
plt.subplot(2, 2, 4)
plt.plot(x, F1)
plt.title("First removal of Tn, then removal of Tp")

plt.show()
