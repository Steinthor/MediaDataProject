import sys
import pickle

# Reference:
# https://stackoverflow.com/questions/19201290/how-to-save-a-dictionary-to-a-file
def save_obj(obj, name):
    with open(name + '.dic', 'wb') as f:
        pickle.dump(obj, f, protocol=0)


def load_obj(name):
    with open(name + '.dic', 'rb') as f:
        return pickle.load(f)

# Reference:
# https://stackoverflow.com/questions/15785719/how-to-print-a-dictionary-line-by-line-in-python
def dump(obj, nested_level=0, output=sys.stdout):
    spacing = '   '
    if type(obj) == dict:
        print('%s{' % ((nested_level) * spacing))5
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print('%s%s:' % ((nested_level + 1) * spacing, k))
                dump(v, nested_level + 1, output)
            else:
                print('%s%s: %s' % ((nested_level + 1) * spacing, k, v))
        print('%s}' % (nested_level * spacing))
    elif type(obj) == list:
        print('%s[' % ((nested_level) * spacing))
        for v in obj:
            if hasattr(v, '__iter__'):
                dump(v, nested_level + 1, output)
            else:
                print('%s%s' % ((nested_level + 1) * spacing, v))
        print('%s]' % ((nested_level) * spacing))
    else:
        print('%s%s' % (nested_level * spacing, obj))


#  START OF ANALYSIS
# load a dictionary from a file
test = load_obj('result00')
#dump(test)

