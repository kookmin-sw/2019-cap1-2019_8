import argparse
import warnings
import utils
import pickle

from malconv import Malconv
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.models import load_model
from os.path import join
from utils import *
from sklearn.model_selection import StratifiedKFold

from settings import *

warnings.filterwarnings("ignore")


BATCH_SIZE = 64
EPOCH = 5
MAX_LEN = 200000
WIN_SIZE = 500

if __name__ == '__main__':

    model = Malconv(MAX_LEN, WIN_SIZE)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy', precision, recall, f1score])

    data, label = get_file_path(TRAIN_PATH)
    valid_data, valid_label = get_file_path(VALID_PATH)
    seed = 7
    np.random.seed(seed)
    # 10 Fold Cross Validation
    kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
    cv_score = []
    cv_f1_score = []
    for i, (trn_idx, val_idx) in enumerate(kfold.split(data, label), start=1):
        print(f"K-FOLD: {i}")

        ear = EarlyStopping(monitor='val_loss', patience=2, mode="auto")
        mcp = ModelCheckpoint(join("../saved/", 'malconv.h5'),
                              monitor="val_loss",
                              save_best_only=True,
                              save_weights_only=False)

        history = model.fit_generator(
            utils.data_generator(data[trn_idx], label[trn_idx], MAX_LEN, BATCH_SIZE, shuffle=True),
            steps_per_epoch=len(data[trn_idx]) // BATCH_SIZE + 1,
            epochs=EPOCH,
            verbose=1,
            callbacks=[ear, mcp],
            # validation_data=utils.data_generator(data[val_idx], label[val_idx], MAX_LEN, BATCH_SIZE),
            # validation_steps=len(data[val_idx]) // BATCH_SIZE + 1)
            validation_data=utils.data_generator(valid_data, valid_label, MAX_LEN, BATCH_SIZE),
            validation_steps=len(valid_data) // BATCH_SIZE + 1)



        _, acc, _, _, _f1score = model.evaluate_generator(utils.data_generator(valid_data, valid_label, MAX_LEN, BATCH_SIZE),
                                          verbose=1, steps=len(valid_data) // BATCH_SIZE + 1)
        # _, acc, _, _, _f1score = model.evaluate_generator(utils.data_generator(valid_data, valid_label, MAX_LEN, BATCH_SIZE),
        #                                   verbose=1, steps=len(data[val_idx]) // BATCH_SIZE + 1)
        print(f"Validation {model.metrics_names[1]}: {acc}")
        print(f"Validation {model.metrics_names[4]}: {_f1score}")

        cv_score.append(acc * 100)
        cv_f1_score.append(_f1score * 100)
    print(f"CV SCORE: {np.mean(cv_score)} | STD : {np.std(cv_score)}")
    print(f"CV F1 SCORE: {np.mean(cv_f1_score)} | STD : {np.std(cv_f1_score)}")
        # history = train(model, args.max_len, args.batch_size, args.verbose, args.epochs, args.save_path, args.save_best)

    # with open(join(args.save_path, 'history.pkl'), 'wb') as f:
    #     pickle.dump(history.history, f)

