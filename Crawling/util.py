import pickle


def pickle_save( path, obj):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)


def pickle_load(path):
    with open(path, 'rb') as f:
        obj = pickle.load(f)
    return obj
