import pickle
import os.path
import numpy as np


def pickle_it(variable, name):
    pickle.dump(variable, open( name, "wb"))

def load_pickle(name):
    return pickle.load(open( name, "rb"))

def pickle_exists(name):
    return os.path.isfile(name)

def build_sim_matrix(documents):
    n = len(documents)
    matrix = np.zeros((n, n), dtype=np.float32)
    for i in range(n):
        for j in range(n):
            matrix[i][j] = ruzicka_similarity(documents[i], documents[j])
        
        if i % 10 == 0:
            print("Calculting similarities. {:.2f}%".format((i / n) * 100))

    return matrix

def jaccard_similarity(documentI, documentJ):
    keys_i = set(documentI['words'].keys())
    keys_j = set(documentJ['words'].keys())
    intersection = keys_i & keys_j

    union = keys_i.copy()
    union.update(keys_j)

    return len(intersection) / len(union)

def ruzicka_similarity(documentI, documentJ):
    keys_i = set(documentI['words'].keys())
    keys_j = set(documentJ['words'].keys())
    union = keys_i.copy()
    union.update(keys_j)

    numerator = 0
    denominator = 0
    for key in union:
        x_i = 0
        j_i = 0

        if key in documentI['tfidf']:
            x_i = documentI['tfidf'][key]
        
        if key in documentJ['tfidf']:
           j_i = documentJ['tfidf'][key]
        
        numerator += min(x_i, j_i)
        denominator += max(x_i, j_i)
    
    return numerator / denominator


documents = load_pickle('sample.bin')
sim_matrix = build_sim_matrix(documents)
pickle_it(sim_matrix, 'sim_matrix.bin')
