import csv
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import operator
import os.path
import pickle
import math

stemmer = PorterStemmer()

DATASET_PATH = '/home/randomhash/datasets/lyrics/songdata.csv'
DELIMITER = ','
QUOTE_CHAR='"'
FIELDS = {
    'ARTIST': 'artist',
    'SONG': 'song',
    'LINK': 'link',
    'TEXT': 'text'
}

REMOVE_SIGNS = [',', '.', '?']

def pickle_it(variable, name):
    pickle.dump(variable, open( name, "wb"))

def load_pickle(name):
    return pickle.load(open( name, "rb"))

def pickle_exists(name):
    return os.path.isfile(name)

def read_dataset():
    document_frequency = {
        'words': {}
    }
    documents = []
    counter = 0

    if(not pickle_exists('documents.bin') or not pickle_exists('document_frequency.bin')):
        with open(DATASET_PATH, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=DELIMITER, quotechar=QUOTE_CHAR)
            for row in reader:
                document = build_document(row[FIELDS['TEXT']])
                document['title'] = row[FIELDS['SONG']] + " By: " + row[FIELDS['ARTIST']]
                document = calc_term_frequency_by_length(document)
                document_frequency = add_document_frequency(document, document_frequency)

                # If you cannot hold all in memory, dump to db instead
                documents.append(document)

                if counter % 100 == 0:
                    print("{} records done. Artist: {}, Song: {}".format(counter, row[FIELDS['ARTIST']], document['title']))
                counter += 1

        document_frequency = calc_idf(document_frequency, len(documents))
        calc_tdidf(documents, document_frequency)
        pickle_it(documents, 'documents.bin')
        pickle_it(document_frequency, 'document_frequency.bin')
    else:
        documents = load_pickle('documents.bin')
        document_frequency = load_pickle('document_frequency.bin')

    print(documents[0]['tfidf'])

def build_document(raw):

    document = {
        'words': {},
        'len': len(raw),
    }

    for word in raw.split(" "):
        _word = word.strip()
        if len(_word) > 0:
            _word = _word.lower()
            for sign in REMOVE_SIGNS:
                _word = _word.replace(sign, '')

            _word = stemmer.stem(_word)

            if _word not in document['words']:
                document['words'][_word] = 0
            
            document['words'][_word] += 1

    return document

def calc_term_frequency_by_length(document):
    document['tf'] = {}

    for word in document['words']:
        document['tf'][word] = document['words'][word] / document['len']
        
    return document

def calc_augmented_term_frequency(document):
    document['tf'] = {}

    maxFPrime = document['words'][max(document['words'], key=document['words'].get)]

    for word in document['words']:
        document['tf'][word] = 0.5 + (0.5 * (document['words'][word] / maxFPrime))
        
    return document

def add_document_frequency(document, document_frequency):
    for word in document['words']:
        if word not in document_frequency['words']:
            document_frequency['words'][word] = 0
        
        document_frequency['words'][word] += 1

    return document_frequency


def calc_idf(document_frequency, n):
    document_frequency['idf'] = {}
    for word in document_frequency['words']:
        document_frequency['idf'][word] = math.log(n / document_frequency['words'][word])


    print(document_frequency)
    return document_frequency

def calc_tdidf(documents, document_frequency):
    counter = 0
    for document in documents:
        document['tfidf'] = {}
        for word in document['words']:
            document['tfidf'][word] = document['tf'][word] * document_frequency['idf'][word]

        if counter % 5000 == 0:
            print("{:.2f}% ".format((counter / len(documents)) * 100))

        counter += 1

read_dataset()
