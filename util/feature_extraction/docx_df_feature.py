import configparser
import os
import zipfile
import numpy as np
import re
import xml.dom.minidom

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

def get_feature_cnt(file_path, file_list):
    result = dict()

    for i in range(len(file_list)):
        try:
            document = zipfile.ZipFile(os.path.join(file_path, file_list[i]))
            features = document.namelist()

            for k in features:
                if k not in result:
                    result[k] = 1
                else:
                    result[k] += 1

        except zipfile.BadZipfile:
            continue

    print(len(result.keys()))
    #print(result)
    return result


def get_feature_df(mal_feature_cnt, ben_feature_cnt, total_fnum):
    result = dict()

    for k in mal_feature_cnt:
        if k in ben_feature_cnt:
            result[k] = mal_feature_cnt[k] + ben_feature_cnt[k]
        else:
            result[k] = 1

    for k in ben_feature_cnt:
        if k in result:
            continue
        else:
            result[k] = 1

    for k in result:
        val = round(result[k] / total_fnum, 3)
        result[k] = val

    return result



def make_feature_vec(file_path, file_list, feature_df):
        total_feature_val = []

        for i in range(len(file_list)):
            result = dict(zip(feature_df, [0 for i in range(len(feature_df))]))
            try:
                # document will be the filetype zipfile.ZipFile
                document = zipfile.ZipFile(os.path.join(file_path, file_list[i]))
                feature = document.namelist()

                for k in result:
                    if k in feature:
                        result[k] = feature_df[k]
                        break

                feature_val = list(result.values())
                total_feature_val.append(feature_val)

            except zipfile.BadZipfile:
                continue

        return total_feature_val

if __name__ == '__main__':
    mal_file_list = make_file_list(mal_file_path)
    ben_file_list = make_file_list(ben_file_path)

    total_fnum = len(mal_file_list) + len(ben_file_list)

    mal_feature_cnt = get_feature_cnt(mal_file_path, mal_file_list)
    ben_feature_cnt = get_feature_cnt(ben_file_path, ben_file_list)

    feature_df = get_feature_df(mal_feature_cnt, ben_feature_cnt, total_fnum)

    #print(len(feature_df.keys()))
    mal_feature_vector = make_feature_vec(mal_file_path, mal_file_list, feature_df)
    ben_feature_vector = make_feature_vec(ben_file_path, ben_file_list, feature_df)
