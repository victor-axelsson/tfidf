import pickle
import os.path
import numpy as np
import csv

def pickle_it(variable, name):
    pickle.dump(variable, open( name, "wb"))

def load_pickle(name):
    return pickle.load(open( name, "rb"))

def pickle_exists(name):
    return os.path.isfile(name)

def format_edges(sim_matrix, documents, threshold):
    edges = []
    n = len(sim_matrix)
    for i in range(n):
        for j in range(n):
            if sim_matrix[i][j] > threshold and i < j:
                edges.append({
                    'Source': documents[i]['title'],
                    'Target': documents[j]['title'],
                    'Weight': sim_matrix[i][j]
                })
    
    return edges

def print_edges_to_csv(edges):
    with open('edges.csv', 'w', newline='') as csvfile:
        fieldnames = ['Source', 'Target', 'Weight']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for edge in edges:
            writer.writerow(edge)
        
similarity = load_pickle('sim_matrix.bin')
documents = load_pickle('sample.bin')
print(similarity.shape)

edges = format_edges(similarity, documents, 0.08)
print_edges_to_csv(edges)



