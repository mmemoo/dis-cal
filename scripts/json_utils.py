import json

def write_json(path,key,val):
    with open(path,"r") as f:
        dict_ = json.load(f)

    dict_[key] = val

    with open(path,"w") as f:
        json.dump(dict_,f)

def read_json(path,key):
    with open(path,"r") as f:
        dict_ = json.load(f)

    return dict_[key]