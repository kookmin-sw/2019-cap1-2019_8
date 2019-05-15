import glob
import numpy as np
import pandas as pd
import tensorflow as tf
import os
from keras import backend as K
from keras.backend.tensorflow_backend import set_session
from dreamav.util.preprocess import preprocess

from sklearn.metrics import f1_score, recall_score, precision_score


def limit_gpu_memory(per):
    config = tf.ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = per
    set_session(tf.Session(config=config))


def train_test_split(data, label, val_size=0.1):
    idx = np.arange(len(data))
    np.random.shuffle(idx)
    split = int(len(data) * val_size)
    x_train, x_test = data[idx[split:]], data[idx[:split]]
    y_train, y_test = label[idx[split:]], label[idx[:split]]
    return x_train, x_test, y_train, y_test


def data_generator(data, labels, max_len=200000, batch_size=64, shuffle=True):
    idx = np.arange(len(data))
    if shuffle:
        np.random.shuffle(idx)
    batches = [idx[range(batch_size * i, min(len(data), batch_size * (i + 1)))] for i in
               range(len(data) // batch_size + 1)]
    while True:
        for i in batches:
            xx = preprocess(data[i], max_len)[0]
            yy = labels[i]
            yield (xx, yy)


def get_file_path(input_path):
    data_path, label = [], []

    label_dict = {}
    for csv_path in glob.glob(os.path.join(input_path, "*.csv")):
        with open(csv_path, "r") as f:
            for line in f.readlines():
                md5, _label = line.strip().split(",")

                label_dict[md5] = int(_label)

    mal, ben = 0, 0
    for path, _, files in os.walk(input_path):
        for file in files:
            md5 = file.split(".")[0]
            if md5 in label_dict:
                data_path.append(os.path.join(path, file))
                label.append(label_dict[md5])

                if label_dict[md5] == 1:
                    mal += 1
                else:
                    ben += 1
    print(f"Mal: {mal}, Ben: {ben}")
    return np.array(data_path), np.array(label)


# def get_file_path(input_path, label_path):
#     result = {}
#     for path, _, files in os.walk(input_path):
#         for file in files:
#             file_path = os.path.join(path, file)
#             result[file.split('.')[0]] = file_path
#
#     df = pd.read_csv(label_path, header=None)
#     df_list = list(zip(df[0].values, df[1].values))
#     data, label = [], []
#
#     for each in df_list:
#         if each[0] in result:
#             data.append(result[each[0]])
#             label.append(each[1])
#
#     return np.array(data), np.array(label)


def recall(y_target, y_pred):
    # clip(t, clip_value_min, clip_value_max) : clip_value_min~clip_value_max 이외 가장자리를 깎아 낸다
    # round : 반올림한다
    y_target_yn = K.round(K.clip(y_target, 0, 1))  # 실제값을 0(Negative) 또는 1(Positive)로 설정한다
    y_pred_yn = K.round(K.clip(y_pred, 0, 1))  # 예측값을 0(Negative) 또는 1(Positive)로 설정한다

    # True Positive는 실제 값과 예측 값이 모두 1(Positive)인 경우이다
    count_true_positive = K.sum(y_target_yn * y_pred_yn)

    # (True Positive + False Negative) = 실제 값이 1(Positive) 전체
    count_true_positive_false_negative = K.sum(y_target_yn)

    # Recall =  (True Positive) / (True Positive + False Negative)
    # K.epsilon()는 'divide by zero error' 예방차원에서 작은 수를 더한다
    # return a single tensor value
    return count_true_positive / (count_true_positive_false_negative + K.epsilon())


def precision(y_target, y_pred):
    # clip(t, clip_value_min, clip_value_max) : clip_value_min~clip_value_max 이외 가장자리를 깎아 낸다
    # round : 반올림한다
    y_pred_yn = K.round(K.clip(y_pred, 0, 1))  # 예측값을 0(Negative) 또는 1(Positive)로 설정한다
    y_target_yn = K.round(K.clip(y_target, 0, 1))  # 실제값을 0(Negative) 또는 1(Positive)로 설정한다

    # True Positive는 실제 값과 예측 값이 모두 1(Positive)인 경우이다
    count_true_positive = K.sum(y_target_yn * y_pred_yn)

    # (True Positive + False Positive) = 예측 값이 1(Positive) 전체
    count_true_positive_false_positive = K.sum(y_pred_yn)

    # Precision = (True Positive) / (True Positive + False Positive)
    # K.epsilon()는 'divide by zero error' 예방차원에서 작은 수를 더한다
    # return a single tensor value
    return count_true_positive / (count_true_positive_false_positive + K.epsilon())


def f1score(y_target, y_pred):
    _recall = recall(y_target, y_pred)
    _precision = precision(y_target, y_pred)
    # K.epsilon()는 'divide by zero error' 예방차원에서 작은 수를 더한다
    # return a single tensor value
    return (2 * _recall * _precision) / (_recall + _precision + K.epsilon())


class logger():
    def __init__(self):
        self.fn = []
        self.len = []
        self.pad_len = []
        self.loss = []
        self.pred = []
        self.org = []

    def write(self, fn, org_score, file_len, pad_len, loss, pred):
        self.fn.append(fn.split('/')[-1])
        self.org.append(org_score)
        self.len.append(file_len)
        self.pad_len.append(pad_len)
        self.loss.append(loss)
        self.pred.append(pred)

        print('\nFILE:', fn)
        if pad_len > 0:
            print('\tfile length:', file_len)
            print('\tpad length:', pad_len)
            # if not np.isnan(loss):
            print('\tloss:', loss)
            print('\tscore:', pred)
        else:
            print('\tfile length:', file_len, ', Exceed max length ! Ignored !')
        print('\toriginal score:', org_score)

    def save(self, path):
        d = {'filename': self.fn,
             'original score': self.org,
             'file length': self.len,
             'pad length': self.pad_len,
             'loss': self.loss,
             'predict score': self.pred}
        df = pd.DataFrame(data=d)
        df.to_csv(path, index=False, columns=['filename', 'original score',
                                              'file length', 'pad length',
                                              'loss', 'predict score'])
        print('\nLog saved to "%s"\n' % path)


