# -*- coding: utf-8 -*-
"""
    Title:          BPG test
    Date:           01.06.2018
    Description:    Demo file how to deal with json file

"""
import json


def save_obj(name, dictionary):
    with open(name + '.json', 'w') as f:
        json.dump(dictionary, f, indent=4)

def load_obj(name):
    with open(name + '.json', 'rb') as f:
        return json.load(f)
    
def dump(dictionary):
    print(json.dumps(dictionary, indent=4))
    

# Create test dictionary
dic = {'Test1': 1, 'Test2': {'SubTest': 'Hallo'}}
save_obj('test', dic)

dic_in = load_obj('test')

dump(dic_in)


