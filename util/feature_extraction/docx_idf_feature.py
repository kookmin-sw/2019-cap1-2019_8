import os
import zipfile
import numpy as np
import re
import math
import xml.dom.minidom


mal_file_path = ''
ben_file_path = ''


def make_file_list(file_path):
    file_list = []
    for root, dirs, files in os.walk(file_path):
        for file in files:
            file_list.append(file)
           # print (file)
    return file_list

def get_feature_cnt(file_path, file_list):
    feature_cnt = dict()
    for i in range(len(file_list)):
        try:
            document = zipfile.ZipFile(os.path.join(file_path, file_list[i]))
            features = document.namelist()

            for k in features:
                if k not in feature_cnt:
                    feature_cnt[k] = 1
                else:
                    feature_cnt[k] += 1

        except zipfile.BadZipfile:
            continue

    #print(len(result.keys()))
    return feature_cnt


def get_feature_df(mal_feature_cnt, ben_feature_cnt, total_fnum, total_feature):
    feature_df = dict(zip(total_feature, [0 for i in range(len(total_feature))]))

    for k in mal_feature_cnt:
        if k in ben_feature_cnt:
            feature_df[k] = mal_feature_cnt[k] + ben_feature_cnt[k]
        else:
            feature_df[k] = 1

    for k in ben_feature_cnt:
        if k in feature_df:
            continue
        else:
            feature_df[k] = 1

    feature_cnt = feature_df.copy() # total docAppear mal+ben
    for k in result:
        val = round(rfeature_df[k] / total_fnum, 3)  # get df value
        feature_df[k] = val

    return feature_cnt, feature_df

def get_feature_idf(feature_cnt, total_fnum):
    feature_idf = dict(zip(total_feature, [0 for _ in range(len(total_feature))]))

    for k in feature_cnt:
        docAppear = feature_cnt[k]  #df value
        val = math.log10(total_fnum / docAppear)
        val = round(val, 3)
        feature_idf[k] = val

    return feature_idf

def make_feature_vec(file_path, file_list, feature_df):
        total_feature_vec = []

        for i in range(len(file_list)):
            result = dict(zip(feature_df, [0 for _ in range(len(feature_df))]))
            try:
                # document will be the filetype zipfile.ZipFile
                document = zipfile.ZipFile(os.path.join(file_path, file_list[i]))
                feature = document.namelist()

                for k in result:
                    if k in feature:
                        result[k] = feature_idf[k]
                        break

                feature_val = list(result.values())
                total_feature_vec.append(feature_val)

            except zipfile.BadZipfile:
                continue

        return total_feature_vec

if __name__ == '__main__':
    mal_file_list = make_file_list(mal_file_path)
    ben_file_list = make_file_list(ben_file_path)

    total_fnum = len(mal_file_list) + len(ben_file_list)

    mal_feature_cnt = get_feature_cnt(mal_file_path, mal_file_list)
    ben_feature_cnt = get_feature_cnt(ben_file_path, ben_file_list)
    total_feature = [set(mal_feature_cnt.keys()) | set(ben_feature_cnt.keys())]

    feature_cnt, feature_df = get_feature_df(mal_feature_cnt, ben_feature_cnt, total_fnum, total_feature)

    mal_feature_vector = make_feature_vec(mal_file_path, mal_file_list, feature_df)
    ben_feature_vector = make_feature_vec(ben_file_path, ben_file_list, feature_df)
