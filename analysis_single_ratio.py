import json
import re
import matplotlib.pyplot as plt
import numpy as np


def save_obj(dictionary, name):
    with open(name + '.json', 'w') as f:
        json.dump(dictionary, f, indent=4)


def load_obj(name):
    with open(name + '.json', 'rb') as f:
        return json.load(f)


def dump(dictionary):
    print(json.dumps(dictionary, indent=4))


#  START OF ANALYSIS
# load all large image dictionary from a directory
test = load_obj('./data/results/large_collection')
#dump(test)

# we need to count true positives, fake positives and fake negatives
# each file has:
# 1) up to 5 different compression scheme
# 2) each compression scheme has different factorisation
# 3) each factorisation has a different keypoint detection 5
# so separate data into compression scheme (ending), detection scheme, factorisation and then Tp, Fp, Fn

anal1 = {}
#analysis['.png']['SURF'][factor]['Tp']
#analysis['.png']['SURF'][factor]['Fp']
#analysis['.png']['SURF'][factor]['Fn']

for file, f_dic in test.items():
    c_scheme = ""

    for comp, c_val in f_dic.items():
        m = re.search(r'(?<=[.])\w+', comp)
        if m:
            c_scheme = comp
            if c_scheme not in anal1:
                anal1[c_scheme] = {}

        if type(c_val) is dict:
            for factor, f_val in c_val.items():
                #print("factor: {0}".format(factor))
                for detector, d_val in f_val.items():
                    result = ""
                    #print("key : {0} , value : {1}".format(detector, d_val))
                    if detector not in anal1[c_scheme]:
                        anal1[c_scheme][detector] = {}
                    if factor not in anal1[c_scheme][detector]:
                        anal1[c_scheme][detector][factor] = {}

                    if 'Tp' not in anal1[c_scheme][detector][factor]:
                        anal1[c_scheme][detector][factor]['Tp'] = 0
                    if 'Tn' not in anal1[c_scheme][detector][factor]:
                        anal1[c_scheme][detector][factor]['Tn'] = 0
                    if 'Fp' not in anal1[c_scheme][detector][factor]:
                        anal1[c_scheme][detector][factor]['Fp'] = 0
                    if 'Fn' not in anal1[c_scheme][detector][factor]:
                        anal1[c_scheme][detector][factor]['Fn'] = 0
                    if f_dic['Fake']:
                        if d_val:
                            result = 'Tp'
                        else:
                            result = 'Fn'
                    else:
                        if d_val:
                            result = 'Fp'
                        else:
                            result = 'Tn'

                    anal1[c_scheme][detector][factor][result] = anal1[c_scheme][detector][factor][result] + 1

#dump(anal1)
Tp_sum = 0
Tn_sum = 0
Fp_sum = 0
Fn_sum = 0
anal2 = {}
anal2['sum'] = {}
for c, c_val in anal1.items():
    for d, d_val in anal1[c].items():
        if d not in anal2['sum']:
            anal2['sum'][d] = {}
        for f, f_val in anal1[c][d].items():
            if f not in anal2['sum'][d]:
                anal2['sum'][d][f] = 0
            Tp = anal1[c][d][f]['Tp']
            Tn = anal1[c][d][f]['Tn']
            Fp = anal1[c][d][f]['Fp']
            Fn = anal1[c][d][f]['Fn']
            if c == '.png' and f == '0':
                Tp_sum = Tp_sum + Tp
                Tn_sum = Tn_sum + Tn
                Fp_sum = Fp_sum + Fp
                Fn_sum = Fn_sum + Fn

            p = 0
            r = 0
            if max(Tp, Fp) > 0:
                p = Tp / (Tp + Fp)
            if max(Tp, Fn) > 0:
                r = Tp / (Tp + Fn)
            if max(p, r) > 0:
                F1 = 2 * p*r / (p+r)
                anal2['sum'][d][f] = anal2['sum'][d][f] + F1

for d, d_val in anal2['sum'].items():
    for f, f_val in anal2['sum'][d].items():
        if f != '0':
            anal2['sum'][d][f] = anal2['sum'][d][f] / 4

fig = plt.figure()
fig.suptitle("F1 Metric for all 4 keypoints at different ratios.")
width = 0.2

print("Tp : {0}, Tn : {1}, Fp : {2}, Fn : {3}".format(Tp_sum, Tn_sum, Fp_sum, Fn_sum))


teljari = 1

comp = '.png'  # This is the compression scheme you want the F1 statistic for
for c in anal2['sum']:
    ax = fig.add_subplot(2, 2, teljari)
    names = list(anal2['sum'][c].keys())
    values = list(anal2['sum'][c].values())
    plt.plot(np.arange(0, values.__len__()), values, marker='o')
    plt.xticks(range(0, values.__len__()), names)

    plt.xlabel("Compression factor")
    plt.ylabel("F1 value")
    plt.ylim(0,1)
    plt.legend()
    plt.title(c)

    plt.tight_layout()
    teljari = teljari + 1

    x = np.arange(-1, 9)
    y = x*0+0.66666
    plt.plot(x, y)
#plt.savefig('metric.png')
plt.show()
