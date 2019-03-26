import configparser
import os
import zipfile
import numpy as np
import re
import xml.dom.minidom #to pretty print our xml

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
config.read('config.ini')

mal_file_path = config.get('PATH', 'MAL_DIR')
ben_file_path = config.get('PATH', 'BEN_DIR')

def make_file_list(file_path):
    file_list = []
    for root, dirs, files in os.walk(file_path):
        for file in files:
            file_list.append(file)
           # print (file)
    return file_list

def make_feature(file_path, file_list):
    features = []
    for i in range(len(file_list)):
        try:
            # document will be the filetype zipfile.ZipFile
            document = zipfile.ZipFile(os.path.join(file_path, file_list[i]))
            f = document.namelist()
            features.append(f)

        except zipfile.BadZipfile:
            continue

    tmp = [y for x in features for y in x]
    feature_set = set(tmp)
    return feature_set


def make_feature_vec(file_path, file_list, total_feature):
        total_feature_val = []
        for i in range(len(file_list)):
            result = dict(zip(total_feature, [0 for i in range(len(total_feature))]))
            try:
                # document will be the filetype zipfile.ZipFile
                document = zipfile.ZipFile(os.path.join(file_path, file_list[i]))
                feature = document.namelist()
                feature_dict = dict(zip(feature, [1 for i in range(len(feature))]))

                for k1 in result:
                    for k2 in feature_dict:
                        if (k1 == k2):
                            result[k1] = 1

                feature_val = list(result.values())
                total_feature_val.append(feature_val)

            except zipfile.BadZipfile:
                continue

        return total_feature_val


if __name__ == "__main__":
    mal_file_list = make_file_list(mal_file_path)
    ben_file_list = make_file_list(ben_file_path)
    print("mal_file_len: ", len(mal_file_list))
    print("ben_file_len: ", len(ben_file_list))

    mal_feature = make_feature(mal_file_path, mal_file_list)
    ben_feature = make_feature(ben_file_path, ben_file_list)
    total_feature = list(mal_feature | ben_feature)

    mal_feature_vector = make_feature_vec(mal_file_path, mal_file_list, total_feature)
    ben_feature_vector = make_feature_vec(ben_file_path, ben_file_list, total_feature)

    print(len(mal_feature_vector[0]))
    print("\n")
    print(len(ben_feature_vector[0]))