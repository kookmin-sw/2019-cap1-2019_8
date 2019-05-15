import os
import time
import pickle
import argparse
import pandas as pd
from keras.preprocessing.sequence import pad_sequences

def preprocess(file_list, max_len):
    '''
    Return processed data (ndarray) and original file length (list)
    '''
    corpus = []
    for file in file_list:
        with open(file, 'rb') as f:
            corpus.append(f.read())

    corpus = [[byte for byte in doc] for doc in corpus]
    len_list = [len(doc) for doc in corpus]
    seq = pad_sequences(corpus, maxlen=max_len, padding='post', truncating='post')

    return seq, len_list