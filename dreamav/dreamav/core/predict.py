import lightgbm as lgb
import numpy as np
import json
import os
import xgboost as xgb
import pickle

from keras.models import load_model
from dreamav.util.utils import *
from dreamav.__init__ import __ROOT__


def model_load(path):
    with open(path, "rb") as f:
        return pickle.load(f)


def predict_pdf(feature):
    lgb_clf = lgb.Booster(model_file=os.path.join(__ROOT__, "util/model/dreamav_lgb.model"))
    xgb_clf = model_load(os.path.join(__ROOT__, "util/model/dreamav_xgb.model"))
    dt_clf = model_load(os.path.join(__ROOT__, "util/model/dreamav_DT.model"))
    rf_clf = model_load(os.path.join(__ROOT__, "util/model/dreamav_RF.model"))

    feature = np.array([feature])
    lgb_output = lgb_clf.predict(feature, num_iteration=lgb_clf.best_iteration)[0]
    xgb_output = xgb_clf.predict(xgb.DMatrix(feature))[0]
    dt_output = dt_clf.predict(feature)[0]
    rf_output = rf_clf.predict(feature)[0]

    return {
        "result": {
            "LightGBM": str(lgb_output),
            "XGBoost": str(xgb_output),
            "DT": str(dt_output),
            "RF": str(rf_output)
        }
    }

def predict_msword(f_list, label, batch_size=64, verbose=1):
    model = load_model(os.path.join(__ROOT__, "util/model/dreamav_doc.h5"), custom_objects={"f1score": f1score, "precision": precision, "recall": recall})
    max_len = model.input_shape[1]

    output = model.predict_generator(
        data_generator(f_list, label, max_len, batch_size, shuffle=False),
        steps=len(f_list) // batch_size + 1,
        verbose=verbose
    )[0][0]

    return {
        "result": {
            "DL": str(output)
        }
    }