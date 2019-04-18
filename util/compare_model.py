import pandas as pd
import lightgbm as lgb
import numpy as np

from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score

data_path = ''

models = []
models.append(("LR", LogisticRegression()))
models.append(("DT", DecisionTreeClassifier()))
models.append(("SVM", SVC()))
models.append(("NB", GaussianNB()))
models.append(("KNN", KNeighborsClassifier()))
models.append(("RF", RandomForestClassifier()))
models.append(("GB", GradientBoostingClassifier()))
models.append(("AB", AdaBoostClassifier()))
models.append(("ANN", MLPClassifier()))


param = {'num_leaves': 64,
         'min_data_in_leaf': 64,
         'objective':'binary',
         'nthread': 1,
         'max_depth': -1,
         'learning_rate': 0.05,
         "boosting": "gbdt",
         "feature_fraction": 0.7,
         "bagging_freq": 1,
         "bagging_fraction": 0.7 ,
         "bagging_seed": 11,
         "metric": ['auc','binary_logloss'],
         "lambda_l1": 0.1,
         "random_state": 24,
         "verbosity": -1}

def get_acc(x_train, y_train):
    for name, model in models:
        model.fit(x_train, y_train)
        y_pred = model.predict(x_train)
        print(name, "'s Accuracy is ", accuracy_score(y_train, y_pred))



def get_cv(x_train, y_train):
    for name, model in models:
        scores = np.mean(cross_val_score(model, x_train, y_train, cv=10))
        print(name, "'s mean cv 10-fold is ", scores)


def run_lgb(x_train, y_train):
    # train
    trn_data = lgb.Dataset(x_train, label=y_train)

    print('Starting training...')
    bst = lgb.train(param, trn_data,
                    num_boost_round=5000,
                    valid_sets=trn_data,
                    verbose_eval=100,
                    early_stopping_rounds=200
                    )

    y_pred = bst.predict(x_train)
    # convert into binary values
    y_pred = [ 1 if x >= 0.5 else 0 for x in y_pred ]
    print("LGB's Accuracy is ", accuracy_score(y_train, y_pred))



if __name__ == "__main__":
    df = pd.read_csv(data_path)
    x_train = df.iloc[:, :-1].values
    y_train = df.iloc[:, -1].values

    get_acc(x_train, y_train)
    get_cv(x_train, y_train)
    run_lgb(x_train, y_train)