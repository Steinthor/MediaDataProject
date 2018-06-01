import json
import re
import matplotlib.pyplot as plt


def save_obj(dictionary, name):
    with open(name + '.json', 'w') as f:
        json.dump(dictionary, f, indent=4)


def load_obj(name):
    with open(name + '.json', 'rb') as f:
        return json.load(f)


def dump(dictionary):
    print(json.dumps(dictionary, indent=4))


#  START OF ANALYSIS
# load a dictionary from a file
test = load_obj('result_2018_06_01__14_26_22')
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

dump(anal1)
anal2 = {}
for c, c_val in anal1.items():
    if c not in anal2:
        anal2[c] = {}
    for d, d_val in anal1[c].items():
        if d not in anal2[c]:
            anal2[c][d] = {}
        for f, f_val in anal1[c][d].items():
            if f not in anal2[c][d]:
                anal2[c][d][f] = 0
            Tp = anal1[c][d][f]['Tp']
            Fp = anal1[c][d][f]['Fp']
            Fn = anal1[c][d][f]['Fn']

            p = 0
            r = 0
            if max(Tp, Fp) > 0:
                p = Tp / (Tp + Fp)
            if max(Tp, Fn) > 0:
                r = Tp / (Tp + Fn)
            if max(p, r) > 0:
                F1 = 2 * p*r / (p+r)
                anal2[c][d][f] = anal2[c][d][f] + F1

for data in anal2['.jpeg']:
#data = anal2['.jpeg']['SIFT']
    names = list(anal2['.jpeg'][data].keys())
    values = list(anal2['.jpeg'][data].values())
    plt.bar(range(0, 7), values, label=data, tick_label=names)
    plt.xticks(range(0, 7), names)
plt.xlabel("Compression factor")
plt.ylabel("F1")
plt.legend()
#plt.savefig('fruit.png')
plt.show()
