import pickle
import os.path
import numpy as np
import random

def pickle_it(variable, name):
    pickle.dump(variable, open( name, "wb"))

def load_pickle(name):
    return pickle.load(open( name, "rb"))

def pickle_exists(name):
    return os.path.isfile(name)

def reservoir_sample(documents, k):
    reservoir = []
    random.shuffle(documents)

    for i in range(k):
        reservoir.append(documents[i])

    for i in range(k, len(documents)):
        j = random.randint(0, i - 1)
        if j < k:
            reservoir[j] = documents[i]
    
    return reservoir

documents = load_pickle('documents.bin')

K = 1000
sample = reservoir_sample(documents, K)
pickle_it(sample, 'sample.bin')

print("Sampled {} into {} random samples".format(len(documents), len(sample)))
