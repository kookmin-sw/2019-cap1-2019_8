import math
import collections
import os
import zipfile
import pickle
import numpy as np

FILE_PATH = r''
SAVE_PATH = r''


def create_file_list(PATH):
    file_list = []
    for root, dirs, files in os.walk(PATH):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


def set_count(file_list):
    m_set = set()
    for i in file_list:
        try:
            # document will be the filetype zipfile.ZipFile
            document = zipfile.ZipFile(i)
            name_list = document.namelist()
            for i in name_list:
                items = i.split('/')
                for i in range(0, len(items)):
                    m_set.add('/'.join(items[i:]))
        except zipfile.BadZipfile:
            continue
    return m_set


def make_table(file_list):
    df_dict = {}
    for i in file_list:
        try:
            document = zipfile.ZipFile(i)
            name_list = document.namelist()

            for i in name_list:
                items = i.split('/')
                for i in range(0, len(items)):
                    df_dict['/'.join(items[i:])] = df_dict.get('/'.join(items[i:]), 0) + 1

        except zipfile.BadZipfile:
            continue

    df_rank_list = sorted(df_dict.items(), key=lambda x: x[1], reverse=True)[:1024]

    df_rank_dict = dict()
    rank = 0

    for k, _ in df_rank_list:
        df_rank_dict[k] = rank
        rank += 1

    return df_rank_dict


def get_entropy(data):
    """Calculate the entropy of a chunk of data."""

    if len(data) == 0:
        return 0.0

    occurences = collections.Counter(bytearray(data))

    entropy = 0
    for x in occurences.values():
        p_x = float(x) / len(data)
        entropy -= p_x * math.log(p_x, 2)

    return entropy


def make_feature_vec(df_rank_dict, file_list):
    for path in file_list:
        try:
            feature_vector = [0 for _ in range(1024)]
            entropy_list = []
            file_size = []

            with zipfile.ZipFile(path) as document:
                name_list = document.namelist()

                for name in name_list:
                    items = name.split('/')
                    for i in range(0, len(items)):
                        k = '/'.join(items[i:])
                        if k in df_rank_dict:
                            feature_vector[df_rank_dict[k]] = 1



                for name in name_list:
                    with document.open(name) as f:
                        data = f.read()
                        entropy_list.append(get_entropy(data))
                        file_size.append(len(data))

                feature_vector += [min(entropy_list), max(entropy_list), np.mean(entropy_list),
                                   os.path.getsize(path), min(file_size), max(file_size), np.mean(file_size)]

            with open(os.path.join(SAVE_PATH, str(os.path.basename(path).split('.')[0])) + '.pk1', 'wb') as f:
                pickle.dump(feature_vector, f)

        except zipfile.BadZipfile:
            continue


if __name__ == "__main__":
    file_list = create_file_list(FILE_PATH)
    df_dict = make_table(file_list)
    make_feature_vec(df_dict, file_list)
